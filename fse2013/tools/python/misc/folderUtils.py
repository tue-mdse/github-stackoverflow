"""Copyright 2012-2013
Eindhoven University of Technology
Bogdan Vasilescu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUD ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

"""Some useful utilities for working with folders"""

import os, glob, ctypes
import fnmatch


class MyFolder:

	def __init__(self, path):
		"""Initialize object
		
		Keyword arguments:
        path -- absolute or relative path to folder
		"""
		self.path = os.path.abspath(path)
		
		
	def path(self):
		return self.path
		
		
	def fullFileNames(self, ext, recursive = None):
		"""Get list of full file names with extension 'ext'
		
		Keyword arguments:
		ext 		-- extension string ('*.txt', '*.java')
		recursive 	-- 1 (look recursively in subfolders) or 0
		"""
		if recursive is None:
			return glob.glob( os.path.join(self.path, ext) )
		else:
			listOfFiles = []
			for path, _, files in os.walk(self.path):
				for f in [os.path.abspath(os.path.join(path, filename)) \
					for filename in files if fnmatch.fnmatch(filename, ext)]:
					listOfFiles.append(f)
			return listOfFiles
		
		
	def baseFileNames(self, ext, recursive = None):
		"""Get list of base file names with extension 'ext'
		
		Keyword arguments:
		ext 		-- extension string ('*.txt', '*.java')
		recursive 	-- 1 (look recursively in subfolders) or 0
		"""
		listOfFiles = []

		if recursive is None:
			files = glob.glob( os.path.join(self.path, ext) )
			for f in files:
				listOfFiles.append(os.path.basename(f))
		else:
			for path, _, files in os.walk(self.path):
				for f in [os.path.abspath(os.path.join(path, filename)) \
					for filename in files if fnmatch.fnmatch(filename, ext)]:
					listOfFiles.append(os.path.basename(f))
			
		return listOfFiles
			

	def create(self):
		"""Create a new folder if it does not already exist
		"""
		if not (os.path.isdir(self.path)):
			os.system("mkdir %s" % self.path)
		return self.path
			
			
	def subfolders(self):
		return os.listdir(self.path)

	def subfoldersNoHidden(self):
	
		def is_hidden(filepath):
			name = os.path.basename(os.path.abspath(filepath))
			return name.startswith('.') or has_hidden_attribute(filepath)
	
		def has_hidden_attribute(filepath):
			try:
				attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
				assert attrs != -1
				result = bool(attrs & 2)
			except (AttributeError, AssertionError):
				result = False
			return result
	
		onlyDirs = []
		for l in os.listdir(self.path):
			fullname = os.path.join(self.path, l)
			if os.path.isdir(fullname):
				if not is_hidden(fullname):
					onlyDirs.append(l)
		return onlyDirs


