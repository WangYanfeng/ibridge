#! /bin/python

from SessionMgmt import *
from Logger import *

def authenticate(func):
    def _authenticate(*args, **kwargs):
	sessionMgmt=SessionMgmt()
	#session_id=kwargs.get("session_id","")
	#user_name=kwargs.get("user_name","")
	session_id=web.cookies().get("session_id")
        user_name=web.cookies().get("user_name")
	session=sessionMgmt.checkSession(session_id,user_name)
	if session:
	    ibLogger.info("authenticate, user_name:[ %s ]",user_name)
	    func(*args, **kwargs)
	else:
	    raise Exception("Authenticate Error")

    return _authenticate

def webkwargs(func):
    def _webkwargs(*args, **kwargs):
	session_id=web.cookies().get("session_id")
        user_name=web.cookies().get("user_name")
	kwargs={"session_id":session_id,"user_name":user_name}
	func(*args, **kwargs)
	
    return _webkwargs

@authenticate
def func(*args, **params):
    print args
    print params

if len(sys.argv) == 2 and sys.argv[1] == "test":
    d={"user_name":"Tom", "session_id":"b9f0710665c02dd909b3c661de689b616d1761e0acda3126c9fecfb064ec9f63"}
    func(**d)
