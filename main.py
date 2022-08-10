def preprocess(img):
	pass
	# Grayscale

	# Threshholding
		# Determine separation line by mean (to handle colored backgrounds/text)
		# Binarize

def process_page(img):
	pass
	# Determine background color
		# Take mode color
	# Handle margins and borders

	# Split into lines

def process_line(img):
	pass
	# Split lines into characters

	# Normalize characters and pass to model
		# Trim white space for each character (in case font size change in line creates extra white space)
		# Add border to form square

def main():
	import os

	try:
		from pdf2image import convert_from_path
	except ModuleNotFoundError:
		print("Error: pdf2image module not found")
	try:
		from PIL import Image
	except ModuleNotFoundError:
		print("Error: PIL module not found")

	path = ""

	img = Image.open(path)
	img = preprocess(img)
	process_page(img)

if __name__ == "main":
	main()
