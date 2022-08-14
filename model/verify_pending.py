"""
Automatically moves all files in pending_dataset to dataset
"""

import os
import shutil

src = 'pending_dataset'
dst = 'dataset'

paths = os.listdir(dst)
for dir in paths:
	preexisting = [int(f[:-4]) for f in os.listdir(dst + os.sep + dir)]
	start_i = max(preexisting) + 1 if preexisting else 0
	for i, file in enumerate(os.listdir(src + os.sep + dir)):
		shutil.move(f'{src}{os.sep}{dir}{os.sep}{file}',
		            f'{dst}{os.sep}{dir}{os.sep}{start_i + i}{file[-4:]}')
