#/usr/bin/env python
import xmlrpclib
import os
import hashlib
import uuid
import pdb
import sys
import StringIO
import zipfile
import base64
import datetime
import pickle
import getopt
import codecs
reload(sys) 
UserHome =  os.path.expandvars('$HOME')
UserDictionary = UserHome + '/.wiznoteuser' 


sys.setdefaultencoding('utf8')
def md5Data(data):
	m = hashlib.md5()
	m.update(data)
	m.digest()
	return m.hexdigest()
class WizAccount:
	def __init__(self,password,userId):
		self.password = password
		self.userId = userId
def checkUserIdVaild(userId):
	if userId == '':
		return False
		pass
	return True
account = WizAccount('aa@aa.com','sss')
if not os.path.exists(UserDictionary):
	userId = raw_input('WizNote UserId :')
	if not checkUserIdVaild(userId):
		print 'User name invalid'
		sys.exit(0)
		pass
	password = raw_input('password:')
	if password == None or password == '':
		print 'password is none'
		sys.exit(0)
		pass
	password = 'md5.' + md5Data(password)
	account.userId = userId
	account.password = password
	addAccountFile = open(UserDictionary,'w')
	pickle.dump(account, addAccountFile, 0)
	addAccountFile.close()
else:
	accountFile = open(UserDictionary,'r')
	account = pickle.load(accountFile)
	accountFile.close()



from wizhelper.WizServerUrl import WizServerUrl

def encodebindata(data):
	out = StringIO.StringIO()
	bin = StringIO.StringIO(data)
	base64.encode(bin,out)
	return out.getvalue()

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


def md5File(name):
	m = hashlib. md5()
	fd = open(name, 'rb')
	m.update(fd.read())
	fd.close()
	return m.hexdigest()
class WizDocument:
	def __init__(self):
		self.guid = '%s' % uuid.uuid1()
		self.data_md5 = ''
		self.document_category = '/My Notes/'
		self.document_attachment_count = 0
		self.document_location = '/My Notes/'
		self.document_protect = 0
		self.document_tag_guids = ''
		self.document_title = 'Python Auto Saved File'
		self.document_type = 'PythonAutoSavedFile'
		self.document_zip_md5 = ''
		self.dt_created = datetime.datetime.today()
		self.dt_modified = self.dt_created 

	def toServerDictionary(self):
		dic = {}
		dic['data_md5'] = self.data_md5
		dic['document_attachment_count'] = self.document_attachment_count
		dic['document_category'] = self.document_category
		dic['document_guid'] = self.guid
		dic['document_location'] = self.document_location
		dic['document_protect'] = self.document_protect
		dic['document_tag_guids'] = self.document_tag_guids
		dic['document_title'] = self.document_title
		dic['document_type'] = self.document_type
		dic['document_zip_md5'] = self.document_zip_md5
		dic['dt_created'] = xmlrpclib.DateTime(self.dt_created)
		dic['dt_modified'] = xmlrpclib.DateTime(self.dt_modified)
		return dic

def addToken(params, token):
	params['token'] = token

def uploadFile(filePath, document_title, document_location):
	fileExist = os.path.exists(filePath)
	if not fileExist :
		print "File not found!"
		return
	#
	document = WizDocument()
	document.data_md5 = md5File(filePath)
	document.title = 'aaa'
	document.document_zip_md5 = document.data_md5;
	if not document_title == None:
		document.document_title = document_title
		pass
	if not document_location == None:
		document.document_location = document_location
		pass
	#
	userId = account.userId
	password = account.password
	loginData = accountLogin(userId, password)
	token = getToken(loginData)
	kbguid = getKbguid(loginData)
	kmUrl = loginData['kapi_url']	
	#
	kmXmlServer = xmlrpclib.Server(kmUrl)
	
	sizehint = 128*1024
	fileSize = os.path.getsize(filePath)
	partCount = fileSize/sizehint+1 if fileSize%sizehint !=0 else fileSize/sizehint
	
	#
	file = open(filePath, 'r')
	position = 0
	lines = file.read(sizehint)
	partSN = 0
	while not file.tell() - position <= 0:
		position = file.tell()
		#
		params ={}
		addCommonParams(params)
		params['obj_size'] = fileSize
		params['part_count'] = partCount
		params['part_sn'] = partSN
		params['data'] = xmlrpclib.Binary(lines)
		params['obj_type']='document'
		params['part_md5'] = md5Data(lines) 
		params['part_size']=len(lines)
		params['obj_guid'] = document.guid
		params['obj_md5'] = document.data_md5
		
		addToken(params, token)
#		pdb.set_trace()
		code = kmXmlServer.data.upload(params)
		###
		lines = file.read(sizehint)
		partSN += 1
	print 'Upload File Succeed!'
	dic = document.toServerDictionary()
	addCommonParams(dic)
	addToken(dic, token)
	dic['with_document_data']=1
	kmXmlServer.document.postSimpleData(dic)
	print 'Upload document info succeed'
def uploadTxtFile(filePath,document_title,document_location):
	zipname = 'temp.ziw'
	e = os.path.exists(zipname)
	if e:
		os.remove(zipname)
	zipFile = zipfile.ZipFile(zipname,'w')
	zipFile.write(filePath,'index.html',zipfile.ZIP_DEFLATED)
	zipFile.close()
	try:
		uploadFile(zipname,document_title,document_location)
	finally:
		os.remove(zipname)

def usage():
	print 'WizNotCommoand -f uploadfilepath -l uploadloaction -h help'
def main():
	try:

		opts, args = getopt.getopt(sys.argv[1:],'f:l:s:h',['file=','location=','string:','help'])
		uploadFile = None
		location = '/My Python Uploaded/'
		uploadStrings = None
		for o , a in opts:
			if o in ('-h','--help'):
				usage()
				pass
			elif o in ('-f', '--file'):
				uploadFile = a
				pass
			elif o in ('-l','--location'):
				location = a 
				pass
			elif o in ('-s', '--string'):
				uploadStrings = a;
				pass
			elif True:
				usage()
			pass
		if uploadFile == None and uploadStrings == None:
			usage()
			sys.exit(0)
			pass
		if uploadFile:
			uploadTxtFile(uploadFile,'asdf',location)
			pass
		if uploadStrings:
			tempFilePath = 'temp.txt'
			if os.path.exists(tempFilePath):
				os.remove(tempFilePath)
			tempFile = codecs.open(tempFilePath,'w','utf-8-sig')
			#pdb.set_trace()
			try:

				tempFile.write(uploadStrings)
				tempFile.close()
				#pdb.set_trace()
				title = uploadStrings.decode('utf8')
				if len(title) > 20:
					title = title[:20]
				uploadTxtFile(tempFilePath,title, location)
				os.remove(tempFilePath)
			except Exception, e:
				raise
			else:
				pass
			finally:
				tempFile.close()
				if os.path.exists(tempFilePath):
					os.remove(tempFilePath)
					pass
				pass
			pass
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

main()

