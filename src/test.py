import xmlrpclib

s = xmlrpclib.Server('http://as.wiz.cn/wizas/xmlrpc')
a = s.accounts.clientLogin({'user_id':'yishuiliunian@gmail.com','password':'654321'})
print a

