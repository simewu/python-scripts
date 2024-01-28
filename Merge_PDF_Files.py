import os
import re
import sys
from PyPDF2 import PdfMerger

def main():
	try:
		while True:
			choice = input('Select by directory (1) or by files (2), or exit (0): ')
			if choice in ['1', '2', '0']:
				break
			print('Invalid choice, please select 1, 2, or 0.')
		
		if choice == '0':
			print('Exiting.')
			return

		pdfs = []
		if choice == '1':
			folder = select_dir(r'.*')
			if folder:
				pdfs = list_files(pdf_regex, folder)
		else:
			pdfs = select_files(pdf_regex)

		if not pdfs:
			print('No PDF files selected. Exiting.')
			return

		merge_pdfs(pdfs)
	except KeyboardInterrupt:
		print("\nScript interrupted by user. Exiting.")
		sys.exit()

# Merges a list of PDFs into one
def merge_pdfs(pdfs):
	merger = PdfMerger(strict=False)
	for pdf in pdfs:
		try:
			print(f'Merging "{pdf}"...')
			with open(pdf, 'rb') as pdf_file:
				merger.append(pdf_file, import_outline=False)
			print(f'"{pdf}" merged successfully.')
		except Exception as e:
			print(f'Failed to merge file "{pdf}": {e}')
			# Decide if you want to continue or break based on the error
			continue  # or break

	output_file = 'MERGED.pdf'
	merger.write(output_file)
	merger.close()
	print('File order:\n' + '\n'.join(pdfs))
	print(f'\nMerged file saved as {output_file}')

# Lists directories matching a given regex, optionally including subdirectories
def select_dir(regex, subdirs = True):
	dirs = []
	if subdirs:
		for root, dirnames, _ in os.walk('.'):
			for dirname in dirnames:
				dirpath = os.path.join(root, dirname)
				if re.match(regex, dirpath):
					dirs.append(dirpath)
	else:
		dirs = [d for d in os.listdir('.') if os.path.isdir(d) and re.match(regex, d)]

	if not dirs:
		print(f'No directories found.\n')
		return ''

	for i, directory in enumerate(dirs, start=1):
		print(f'  Directory {i}  -  {directory}')
	print()

	while True:
		try:
			selection = int(input('Please select a directory: '))
			if 1 <= selection <= len(dirs):
				return dirs[selection - 1]
		except ValueError:
			print('Invalid input, please enter a number.')

# Lists files in a directory matching a given regex, optionally including subdirectories
def select_files(regex, subdirs = True):
	files = list_files(regex, '.', subdirs)
	if not files:
		print('No files found.\n')
		return []

	for i, file in enumerate(files, start=1):
		print(f'  File {i}  -  {file}')
	print()

	selected_files = []
	while not selected_files:
		input_str = input('Please select files (e.g., 1,3,5): ')
		selections = re.split(r',\s*|\s+', input_str)

		for selection in selections:
			try:
				index = int(selection) - 1
				if 0 <= index < len(files):
					selected_files.append(files[index])
			except ValueError:
				pass

		if not selected_files:
			print('Invalid selection, please try again.')

	return selected_files

# Lists files in a directory matching a given regex, optionally including subdirectories
def list_files(regex, directory, subdirs = True):
	files = []
	if subdirs:
		for root, _, filenames in os.walk(directory):
			for filename in filenames:
				filepath = os.path.join(root, filename)
				if regex.match(filename):
					files.append(filepath)
	else:
		path = os.path.abspath(directory)
		files = [os.path.join(path, file) for file in os.listdir(path) 
				 if os.path.isfile(os.path.join(path, file)) and regex.match(file)]
	return files

# Function to clear the screen
def clear_screen():
	# Windows
	if os.name == 'nt':
		_ = os.system('cls')
	# Mac and Linux
	else:
		_ = os.system('clear')

if __name__ == '__main__':
	pdf_regex = re.compile(r'^[^\.]+\.pdf$')  # Precompile regex
	clear_screen()
	main()
	print('Goodbye.')
