# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
import os, re, shutil, json, desktop, utility

# Script directory
base_path = os.path.dirname(os.path.realpath(__file__)) # Location of script

# Daily pose

# Template funtionality
class Template(object):
	def __init__(self):
		self.path = os.path.join( base_path, "template" ) # Path for storing template file
		if not os.path.exists( self.path ):
			os.makedirs( self.path )

	def copy(self, path):
		if os.path.exists( self.path ):
			try:
				shutil.copytree( self.path , path )
				return ""
			except Exception as e:
				return e
		else:
			return "File already exists."


class Data(object):
	def __init__(self):
		self.path = os.path.join( base_path, "data.json" ) # Path for storing data file
		if not os.path.exists( self.path ):
			open( self.path, "w").close()

	def load(self):
		try:
			f = open( self.path, "r" )
			data = json.load( f )
			f.close()
			Data["error"] = ""
			return data
		except Exception as e:
			return {"error": e}

	def save(self, data):
		try:
			f = open( self.path, "w" )
			json.dump( data, f, encoding="utf-8", indent=4 )
			f.close()
			return ""
		except Exception as e:
			return e



for line in utility.list( base_path ):
	print line