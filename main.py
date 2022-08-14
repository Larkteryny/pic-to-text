def preprocess(img):
	dims = img.size

	# Grayscale
	img = img.getdata()
	img = img.convert('L')
	img = list(img)

	# Normalize background/text colors
	# Determine background color
		# Take mode color
	# Handle transparent pixels (PIL ignores alpha channel when converting)
	# Handle margins and borders

	# Threshholding + Binarize
	threshhold = np.mean(img) * 0.8
	img = [int(pixel < threshhold) for pixel in img]
	# 2D
	img = [img[i:i + dims[0]] for i in range(0, dims[0] * dims[1], dims[0])]

	return img

def process_page(img):
	line_img = []

	for l in img:
		if any(l):
			line_img.append(l)
		elif line_img:
			process_line(line_img)
			line_img.clear()

	# Determine blank lines by:
		# Average height of lines (text only, ignore all blank rows)
		# Integer divide all blank sections by avg height

def process_line(img):
	pass
	# Split lines into characters

	# Normalize characters and pass to model
		# Trim white space for each character (in case font size change in line creates extra white space)
		# Add border to form square
		# Resize?

	# Replace all 2 apostrophes with quote

def main():
	import os

	try:
		from pdf2image import convert_from_path
	except ModuleNotFoundError:
		print("Error: pdf2image module not found")
		return
	try:
		import PIL
		from PIL import Image
	except ModuleNotFoundError:
		print("Error: PIL module not found")
		return

	path = ""

	try:
		img = Image.open(path)
	except FileNotFoundError:
		print(f"File count not be found: {path}")
		return
	except PIL.UnidentifiedImageError:
		print("File cannot be opened and identified: path")
		return

	img = preprocess(img)
	process_page(img)

if __name__ == "main":
	main()
