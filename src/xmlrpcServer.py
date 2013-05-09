import xmlrpclib
import os
import hashlib
import uuid
import pdb
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

from wizhelper.WizServerUrl import WizServerUrl
def addCommonParams(postParams):
	postParams['client_type']='python_command'
	postParams['program_type']='normal'
	postParams['api_version']=4


def accountLogin(userId, password):
	s = xmlrpclib.Server(WizServerUrl())
	dic = {}
	dic['user_id']= userId
	dic['password'] = password
	addCommonParams(dic)
	return s.accounts.clientLogin(dic)
def getToken(loginData):
	return loginData['token']
def getKbguid(loginData):
	return loginData['kb_guid']

def md5Data(data):
	m = hashlib.md5()
	m.update(data)
	m.digest()
	return m.hexdigest()
def md5File(name):
	m = hashlib. md5()
	fd = open(name, 'rb')
	m.update(fd.read())
	fd.close()
	return m.hexdigest()
class WizDocument:
	def __init__(self):
		self.guid = uuid.uuid1().hex 

def addToken(params, token):
	params['token'] = token

def uploadFile(filePath):
	fileExist = os.path.exists(filePath)
	if not fileExist :
		print "File not found!"
		return
	#
	document = WizDocument()
	document.dataMd5 = md5File(filePath)
	#
	userId = 'yishuiliunian@gmail.com'
	password = '654321'
	loginData = accountLogin(userId, password)
	token = getToken(loginData)
	kbguid = getKbguid(loginData)
	kmUrl = loginData['kapi_url']	
	#
	kmXmlServer = xmlrpclib.Server(kmUrl)
	print kmXmlServer
	#
	sizehint = 128*1024
	fileSize = os.path.getsize(filePath)
	partCount = fileSize/sizehint+1 if fileSize%sizehint !=0 else fileSize/sizehint
	print "total count %d" % partCount
	#
	file = open(filePath, 'r')
	position = 0
	lines = file.read(sizehint)
	partSN = 0
	while not file.tell() - position <= 0:
		position = file.tell()
		print position
		#
		params ={}
		addCommonParams(params)
		params['obj_size'] = fileSize
		params['part_count'] = partCount
		params['part_sn'] = partSN
		params['data'] = xmlrpclib.Binary(lines)
		params['obj_type']='document'
		params['part_md5'] = md5Data(lines) 
		params['obj_guid'] = document.guid
		params['obj_md5'] = document.dataMd5
		print params
		addToken(params, token)
		pdb.set_trace()
		code = kmXmlServer.data.upload(params)
		###
		lines = file.read(sizehint)
		partSN += 1
	
uploadFile('a.txt')
