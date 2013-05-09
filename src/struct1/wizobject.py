import sys
sys.path.append("..")
import uuid
from wizhelper.WizServerUrl import WizServerUrl
##
class WizObject:
	'''wizobject'''
	def __init__(self):
	    self.guid = uuid.uuid1()
	def printWizObject(self):
		print(self.guid)
print(WizServerUrl())

