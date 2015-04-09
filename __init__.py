# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
import os, re, shutil

# Script directory
base_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join( base_path, "template" )

# If template file doesn't exist. Create one.
if not os.path.exists( template_path ):
	os.makedirs( template_path )
	print "Template file created. Add in files you wish to have in each pose. %s" % template_path

