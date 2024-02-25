import os
import re
import sys

# Given a regular expression, list the directories that match it, and ask for user input to select one or more of them
def selectDir(regex, subdirs=False, multiSelect=False):
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

		selectionPrompt = 'Please select directories (e.g., "1,3-5,9-7,10" for "1,3,4,5,9,8,7,10"): ' if multiSelect else 'Please select a directory: '
		if multiSelect:
			selectedDirs = []
			while not selectedDirs:
				inputStr = input(selectionPrompt)
				selections = re.split(r',\s*|\s+', inputStr)
				addedIndexes = set()

				for selection in selections:
					if '-' in selection:
						parts = selection.split('-')
						try:
							start = int(parts[0]) - 1
							end = int(parts[1]) - 1
							step = 1 if start <= end else -1
							for index in range(start, end + step, step):
								if 0 <= index < len(dirs) and index not in addedIndexes:
									selectedDirs.append(dirs[index])
									addedIndexes.add(index)
						except ValueError:
							pass
					else:
						try:
							index = int(selection) - 1
							if 0 <= index < len(dirs) and index not in addedIndexes:
								selectedDirs.append(dirs[index])
								addedIndexes.add(index)
						except ValueError:
							pass

				if not selectedDirs:
					print('Invalid selection, please try again.')

			return selectedDirs
		else:
			while True:
				selection = input(selectionPrompt)
				if '-' in selection:
					print('Range selection is not supported in single select mode.')
					continue
				try:
					selection = int(selection)
					if 1 <= selection <= len(dirs):
						return dirs[selection - 1]
				except ValueError:
					print('Invalid selection, please try again.')
	except KeyboardInterrupt:
		print("\nOperation cancelled by user.")
		sys.exit()

# Lists files in a directory matching a given regex, optionally including subdirectories
def listFiles(regex = '.*', directory = '', subdirs = True):
	files = []
	if subdirs:
		for root, _, fileNames in os.walk(directory):
			for fileName in fileNames:
				filePath = os.path.join(root, fileName)
				if re.match(regex, fileName):
					files.append(filePath)
	else:
		path = os.path.abspath(directory)
		files = [os.path.join(path, file) for file in os.listdir(path) 
				 if os.path.isfile(os.path.join(path, file)) and re.match(regex, file)]
	return files

directory = selectDir(r'.*', False)
print(f'You selected "{directory}".')
