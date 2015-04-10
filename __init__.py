# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
import os, re, shutil, json, cPickle

# Script directory
base_path = os.path.dirname(os.path.realpath(__file__)) # Location of script

# Template funtionality
class Template(object):
	def __init__(self):
		self.path = os.path.join( base_path, "template" ) # Path for storing template file
		if not os.path.exists( self.path ):
			os.makedirs( self.path )

class Data(object):
	def __init__(self):
		self.path = os.path.join( base_path, "data.json" ) # Path for storing data file
		if not os.path.exists( self.path ):
			open( self.path, "w").close()

	def load(self):
		try:
			return json.load( self.path )
		except e:
			print "ERROR:", e
			return {}

	def save(self, data):
		try:
			f = open( self.path )
			json.dump( data, f, encoding="utf-8", indent=4 )
			f.close()
			return True
		except e:
			print "Could not save data:", e
			return False


class DailyPose(object):
	def __init__(self):
		self.pose_dir = "" # directory for storing poses
		self.loadData()
		self.saveData()

	# load stored data
	def loadData(self):
		try:
			data = json.load( data_path )
			self.pose_dir = data["pose_dir"]
			print "success"
		except:
			pass

	def saveData(self):
		data = {"pose_dir":123}

		f = open( data_path, "w" )
		json.dump( ["data"], f, encoding="utf-8", indent=True )
		f.close()

		

DailyPose()