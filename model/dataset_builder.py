#from pdf2image import convert_from_path
from PIL import Image
import os
import numpy as np

def preprocess(img, txt_color):
	"""Perform preprocessing on image

	:param PIL.Image img: image to preprocess
	:param int txt_color: 0 (black) or 1 (white) indicating text color
	:return 2d-list: binarized rows of white text on black
	"""

	dims = img.size

	# Grayscale
	img = img.getdata()
	img = img.convert('L')
	img = list(img)

	# Invert background/text colors
	if txt_color:
		img = [255 - pixel for pixel in img]

	# Thresholding + Binarize
	threshold = np.mean(img) * 0.8  ################################### * 0.8 is not good #############################
	img = [int(pixel < threshold) for pixel in img]
	# 2D
	img = [img[i:i + dims[0]] for i in range(0, dims[0] * dims[1], dims[0])]

	return img

def process_page(img, text):
	"""Split image into lines

	:param 2d-list img: image to split into lines
	:param text: filepath of corresponding text of image, split into lines with no blank lines
	:return: None
	"""

	with open(text, 'r') as f:
		txt = [l.strip().replace(' ', '') for l in f.readlines() if l.strip()]
	line_img = []
	line_i = 0

	for l in img:
		# Add empty pixels along bottom and right so that no index handling is needed
		if any(l):
			line_img.append(l + [0])
		elif line_img:
			line_img.append([0 for _ in range(len(line_img[0]))])
			process_line(line_img, txt[line_i], line_i)
			line_img.clear()
			line_i += 1

def process_line(img, txt, line_i):
	"""Isolate characters in line and save to pending_dataset

	:param 2d-list img: image containing one line of text
	:param str txt: corresponding line of text
	:return: None
	"""
	def flood(y, x):
		"""Allows for more readable code below"""
		temp.append((y, x))
		img[y][x] = 0
	
	class Shape():
		def __init__(self, img):
			self.pixels = len(img)
			self.img = set(img)
			self.y_min, self.y_max, self.x_min, self.x_max = img[0][0], img[0][0], img[0][1], img[0][1]
			self.y_mean, self.x_mean = 0, 0
			for px in img:
				if px[0] < self.y_min: self.y_min = px[0]
				elif px[0] > self.y_max: self.y_max = px[0]
				if px[1] < self.x_min: self.x_min = px[1]
				elif px[1] > self.x_max: self.x_max = px[1]
				self.y_mean += px[0]
				self.x_mean += px[1]
			self.y_mean /= self.pixels
			self.x_mean /= self.pixels

		def join(self, shape):
			'''Merge two shapes'''

			self.y_mean = np.average((self.y_mean, shape.y_mean), weights=(self.pixels, shape.pixels))
			self.x_mean = np.average((self.x_mean, shape.x_mean), weights=(self.pixels, shape.pixels))
			self.y_min, self.y_max = min(self.y_min, shape.y_min), max(self.y_max, shape.y_max)
			self.x_min, self.x_max = min(self.x_min, shape.x_min), max(self.x_max, shape.x_max)
			self.pixels += shape.pixels
			self.img = self.img.union(shape.img)

			shapes.remove(shape)
			

	# Split lines into characters (left to right)
	shapes = []
	# Left to right scan
	for x in range(len(img[0])):
		for y in range(len(img)):
			if img[y][x]:
				# Find island via flood-fill
				shape = []
				check = [(y, x)]
				img[y][x] = 0

				while check:
					shape += check
					temp = []
					for px in check:
						# Replace all x, y with px[1], px[0]
						if img[px[0] - 1][px[1] - 1]: flood(px[0] - 1, px[1] - 1)
						if img[px[0] - 1][px[1]]: flood(px[0] - 1, px[1])
						if img[px[0] - 1][px[1] + 1]: flood(px[0] - 1, px[1] + 1)
						if img[px[0]][px[1] - 1]: flood(px[0], px[1] - 1)
						if img[px[0]][px[1] + 1]: flood(px[0], px[1] + 1)
						if img[px[0] + 1][px[1] - 1]: flood(px[0] + 1, px[1] - 1)
						if img[px[0] + 1][px[1]]: flood(px[0] + 1, px[1])
						if img[px[0] + 1][px[1] + 1]: flood(px[0] + 1, px[1] + 1)
					check = temp
				shapes.append(Shape(shape))

	# Combine islands who horizontally encompasses another's mean for i, :, =, ?, %
	shapes.sort(key=lambda s: (s.x_mean, s.pixels))
	i = 0
	while i < len(shapes):
		s = shapes[i]
		if i < len(shapes) - 1:
			if shapes[i + 1].x_mean < s.x_max: s.join(shapes[i + 1])
			# Special case for "
			if shapes[i + 1].y_max < len(img) / 2 and s.y_max < len(img) / 2 and\
					abs((shapes[i + 1].x_max - shapes[i + 1].x_min) - (shapes[i + 1].x_min - s.x_max)) < 2 and\
					abs((shapes[i + 1].x_min - s.x_max) - (s.x_max - s.x_min)) < 2:
				s.join(shapes[i + 1])
		if i > 0:
			if shapes[i - 1].x_mean > s.x_min:
				s.join(shapes[i - 1])
				i -= 1
		i += 1

	# Recreate characters
	for i, s in enumerate(shapes):
		# Ignore BACKTICK
		if txt[min(i, len(txt) - 1)] in "`": continue

		# Add border to form square
		if s.x_max - s.x_min < s.y_max - s.y_min:
			addend = [0 for _ in range((s.y_max - s.y_min) - (s.x_max - s.x_min))]
			img = [[1 if (y, x) in s.img else 0 for x in range(s.x_min, s.x_max + 1)] + addend
					for y in range(s.y_min, s.y_max + 1)]
		else:
			addend = [0 for _ in range(s.x_min, s.x_max + 1)]
			img = [[1 if (y, x) in s.img else 0 for x in range(s.x_min, s.x_max + 1)]
					for y in range(s.y_min, s.y_max + 1)] +\
					[addend for _ in range((s.x_max - s.x_min) - (s.y_max - s.y_min))]

		print(len(img), len(img[0]))
		if len(img) != len(img[0]):
			print(*img, sep="\n")
			assert(False)
		new_img = Image.new('L', (len(img), len(img[0])))
		# Flatten
		img = [img[y][x] * 255 for y in range(len(img)) for x in range(len(img[0]))]
		new_img.putdata(img)
		new_img = new_img.resize((28, 28))
		# Place into pending_dataset
		p = os.path.join("pending_dataset", str(ord(txt[min(i, len(txt) - 1)])), f"{line_i}_{i}.jpg")
		print(p)
		new_img.save(p)

def main():
	img_path = os.path.join("passages", "2.jpg")
	txt_path = os.path.join("passages", "2.txt")
	txt_color = 0  # 0: black; 1: white

	img = Image.open(img_path)
	img = preprocess(img, txt_color)
	process_page(img, txt_path)

if __name__ == "__main__":
	main()
