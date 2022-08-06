try:
	from pdf2image import convert_from_path
except ModuleNotFoundError:
	print("Error: pdf2image module not found")
try:
	from PIL import Image
except ModuleNotFoundError:
	print("Error: PIL module not found")
