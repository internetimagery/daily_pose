# Daily pose
import datetime

class Pose(object):

	def __init__(self):
		self.date = datetime.date.today()
		print self.date