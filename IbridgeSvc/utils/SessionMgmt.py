#!/bin/python

"""

"session_id":{
    "user_name":"",
    "app_name":"",
    "dead_time":""
}

"""
import json
import time
import types
import hashlib
from MemManage import MemMgmt

class SessionMgmt(object):
    __instance=None
    __memcacheMgmt=None

    def __new__(cls, *args, **kwargs):
	if not cls.__instance:
            cls.__instance = super(SessionMgmt, cls).__new__(cls, *args, **kwargs)
	    SessionMgmt.__memcacheMgmt=MemMgmt()
        return cls.__instance

    def __init__(self,app_name,valid_time):
	if not type(valid_time) is types.IntType:
	    raise Exception("valid_time not int error")
	self.app_name=app_name
	self.valid_time=valid_time

    def saveSession(self,user_name):
	session=dict()
	session_value={}
	session_value["app_user"]=self.app_name+"_"+user_name
	session_value["dead_time"]=int(time.time())+self.valid_time
	session_key=hashlib.sha256(str(session_value)).hexdigest()
	session[session_key]=session_value
	
	print session
	SessionMgmt.__memcacheMgmt.set(session_key,session_value)
	return session_key
	
    def checkSession(self,session_id,user_name):
	session_value=SessionMgmt.__memcacheMgmt.get(session_id)
	if not session_value:
	    return False
	time_now=time.time()
	if session_value["app_user"] == self.app_name+"_"+user_name:
	    if time_now<session_value["dead_time"]:
	    	return True
	    else:
		self.deleteSession(session_id)
		return False
	return False

    def deleteSession(self,session_id):
	SessionMgmt.__memcacheMgmt.set(session_id,None)

if __name__=="__main__":
    try:
    	session1=SessionMgmt("ibridge",8)
    	id=session1.saveSession("Tom")
	result = session1.checkSession(id,"Tom")
	print result
	print "...sleep..."
	time.sleep(12)
	result = session1.checkSession(id,"Tom")
	print result
    except Exception , e:
	print e
