import os
import re
import sys

# Given a regular expression, list the directories that match it, and ask for user input
def selectDir(regex, subdirs = False, multiSelect = False):
	try:
		dirs = []
		compiledRegex = re.compile(regex)
		if subdirs:
			for dirPath, _, _ in os.walk('.'):
				dirPath = os.path.normpath(dirPath)
				if compiledRegex.match(dirPath):
					dirs.append(dirPath)
		else:
			for obj in os.listdir(os.curdir):
				if os.path.isdir(obj) and compiledRegex.match(obj):
					dirs.append(obj)

		if not dirs:
			print(f'No directories were found that match "{regex}"\n')
			return [] if multiSelect else ''

		print('List of directories:')
		for i, directory in enumerate(dirs):
			print(f'  Directory {i + 1}  -  {directory}')
		print()

		selectionPrompt = 'Please select directories (e.g., 1,3,5): ' if multiSelect else 'Please select a directory: '
		if multiSelect:
			selectedDirs = []
			while not selectedDirs:
				inputStr = input(selectionPrompt)
				selections = re.split(r',\s*|\s+', inputStr)

				for selection in selections:
					try:
						index = int(selection) - 1
						if 0 <= index < len(dirs):
							selectedDirs.append(dirs[index])
					except ValueError:
						pass

				if not selectedDirs:
					print('Invalid selection, please try again.')

			return selectedDirs
		else:
			while True:
				selection = int(input(selectionPrompt))
				if 1 <= selection <= len(dirs):
					return dirs[selection - 1]
	except KeyboardInterrupt:
		print("\nOperation cancelled by user.")
		sys.exit()

# Lists files in a directory matching a given regex, optionally including subdirectories
def listFiles(regex, directory = '', subdirs = True):
	files = []
	if subdirs:
		for root, _, fileNames in os.walk(directory):
			for fileName in fileNames:
				filePath = os.path.join(root, fileName)
				if regex.match(fileName):
					files.append(filePath)
	else:
		path = os.path.abspath(directory)
		files = [os.path.join(path, file) for file in os.listdir(path) 
				 if os.path.isfile(os.path.join(path, file)) and regex.match(file)]
	return files

directory = selectDir(r'.*', False)
print(f'You selected "{directory}".')