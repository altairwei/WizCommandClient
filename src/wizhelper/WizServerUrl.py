import httplib

serverurl = "aaa"

def WizServerUrl():
	global serverurl
	if cmp(serverurl, "aaa")!=0:
		print('aadsfasdfasdf')
		return serverurl
	version = 1.0
	debug = 1
	plat = 'ios'
	url = "api.wiz.cn"
	dir = " /?p=wiz&v=%d&c=sync_http&plat=%s&debug=%d" % (version, plat, bool(debug))
	connection = httplib.HTTPConnection(url,80)
	connection.request('GET',dir)
	serverurl =  connection.getresponse().read()
	connection.close()
	return serverurl
