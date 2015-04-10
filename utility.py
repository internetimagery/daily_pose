# Helper utility functions
import os, re

# List all files in directory
def list( path, hidden = False ): # Show hidden?
	result = []
	regex = re.compile( "%s/?" % path ) # Remove base path for relative URL's
	for root, dirs, files in os.walk(path):
		# Don't go into hidden folders
		for dir in dirs:
			if dir[0] == "." and hidden == False:
				dirs.remove(dir)
		root = re.sub( regex, "", root )
		for file in files:
			# Ignore hidden files
			if not file[0] == "." or hidden:
				result.append( os.path.join( root, file ) )
	return result