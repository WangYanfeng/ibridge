#!/bin/python

"""
    "sessions":[session_id1,session_id2],
    "session_id1":{
    	"user_id":"",
    	"user_name":"",
    	"app_name":"",
    	"dead_time":""
    }
"""
import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

import time
import types
import hashlib
import ConfigParser
from utils.Logger import *
from MemManage import MemMgmt
from entity.Session import Session

class SessionMgmt(object):
    __instance=None
    __memcacheMgmt=None

    def __new__(cls, *args, **kwargs):
	if not cls.__instance:
            cls.__instance = super(SessionMgmt, cls).__new__(cls, *args, **kwargs)
	    SessionMgmt.__memcacheMgmt=MemMgmt()
        return cls.__instance

    def __init__(self):
	config = ConfigParser.ConfigParser()
        config.readfp(open('/usr/ibridge/IbridgeSvc/conf/config.ini'))
	self.interval = config.get("Session","interval")
	self.app_name = config.get("Session","app_name")

    def saveSession(self,user_name,user_id):
	session=Session(user_id,user_name,self.app_name,self.interval)
	
	session_id=hashlib.sha256(session.getSessionStr()).hexdigest()
	session.setSessionId(session_id)
	SessionMgmt.__memcacheMgmt.set(session_id,session)
	
	sessions=SessionMgmt.__memcacheMgmt.get("sessions")
	if not sessions:
	    sessions=[]
	sessions.append(session_id)
	SessionMgmt.__memcacheMgmt.set("sessions",sessions)
	
	ibLogger.info("save session, session_id:[ %s ] interval:[ %s ]",session_id,self.interval)
	return session
	
    def __updateSessionTime(self,session_id):
	session=SessionMgmt.__memcacheMgmt.get(session_id)
	session.setDeadTime(int(time.time())+int(self.interval))
	
	SessionMgmt.__memcacheMgmt.set(session_id,session)

    def checkSession(self,session_id,user_name):
	if not (session_id and user_name):
	    return False
	self.purge()
	session=SessionMgmt.__memcacheMgmt.get(session_id)
	if not session:
	    return False
	time_now=time.time()
	if session.getAppName() == self.app_name:
	    if time_now<session.getDeadTime():
		self.__updateSessionTime(session_id)
		return session
	    else:
		self.deleteSession(session_id)
		return False
	return False

    def deleteSession(self,session_id):
	sessions=SessionMgmt.__memcacheMgmt.get("sessions")
	if session_id in sessions:
	    SessionMgmt.__memcacheMgmt.set(session_id,None)
	    
	    sessions.remove(session_id)
	    SessionMgmt.__memcacheMgmt.set("sessions",sessions)
	    ibLogger.info("delete session, session_id:[ %s ]",session_id)

    def purge(self):
	sessions=SessionMgmt.__memcacheMgmt.get("sessions")
	if not sessions:
	    return
	for s in sessions:
	    session_data=SessionMgmt.__memcacheMgmt.get(s)
	    if not session_data:
		sessions.remove(s) 
	    if session_data and session_data.getDeadTime() < time.time():
		SessionMgmt.__memcacheMgmt.set(s,None)
		sessions.remove(s)
		ibLogger.info("delete timeout session, session_id:[ %s ]",s)
	SessionMgmt.__memcacheMgmt.set("sessions",sessions)

    def getAllSessionId(self):
	sessions=SessionMgmt.__memcacheMgmt.get("sessions")
	return sessions

    def getSessionById(self,session_id):
	session=SessionMgmt.__memcacheMgmt.get(session_id)
	#session=Session(user_id=session["user_id"],user_name=session["user_name"],app_name=session["app_name"],interval=self.interval,dead_time=session["dead_time"],session_id=session_id)
	return session

if __name__=="__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "getSessions":
    	session1=SessionMgmt()
	sessions=session1.getAllSessionId()
	print sessions
    elif len(sys.argv) == 3 and sys.argv[1] == "get":
    	session1=SessionMgmt()
	s=session1.getSessionById(sys.argv[2])
	print s.getSessionStr()
    elif len(sys.argv) == 3 and sys.argv[1] == "set":
    	session1=SessionMgmt()
	s=session1.saveSession(sys.argv[2],1)
	print s.getSessionId()
    elif len(sys.argv) == 4 and sys.argv[1] == "checkSession":
    	session1=SessionMgmt()
	s=session1.checkSession(sys.argv[2],sys.argv[3])
	print s
    elif len(sys.argv) == 2 and sys.argv[1] == "purge":
    	session=SessionMgmt()
	session.purge()
    elif len(sys.argv) == 2 and sys.argv[1] == "test":
	try:
    	    session1=SessionMgmt()
    	    session=session1.saveSession("Tom",1)
	    result = session1.checkSession(session.getSessionId(),"Tom")
	    print "...sleep..."
	    time.sleep(3)
	    result = session1.checkSession(session.getSessionId(),"Tom")
	    print result
    	except Exception , e:
	    print e
