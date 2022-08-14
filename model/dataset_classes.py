"""
Automatically creates/deletes folders for specified characters
When deleting, relocates files to unwanted_dataset for ease of deletion/recovery
"""

import os
import shutil

mode = 0  # 0: create; 1: delete

# All ASCII printable characters (excluding SPACE)
chars = [str(x) for x in range(33, 127)]
paths = ['dataset', 'pending_dataset']

if mode:
	for c in chars:
		if not os.path.isdir(paths[0] + os.sep + c):
			chars.remove(c)

	for path in paths:
		new_path = 'unwanted_dataset' + os.sep + path
		for c in chars:
			shutil.move(path + os.sep + c, new_path + os.sep + c)

else:
	for path in paths:
		for c in chars:
			os.makedirs(path + os.sep + c, exist_ok=True)
