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

import json
import time

class Session(object):
    def __init__(self,user_id,user_name,app_name,interval,dead_time=0,session_id=0):
	self.user_id=user_id
	self.user_name=user_name
	self.app_name=app_name
	self.interval=interval
	self.dead_time=dead_time
	self.session_id=session_id

    def getUserId(self):
	return self.user_id

    def getUserName(self):
	return self.user_name

    def getAppName(self):
	return self.app_name

    def getInterval(self):
	return self.interval

    def getSessionId(self):
	return self.session_id

    def getDeadTime(self):
	return self.dead_time

    def setSessionId(self,session_id):
	self.session_id=session_id

    def setDeadTime(self,dead_time):
	self.dead_time=dead_time

    def getSessionStr(self):
	self.dead_time=int(time.time())+int(self.interval)
	session_value={}
        session_value["user_id"]=self.user_id
        session_value["user_name"]=self.user_name
        session_value["app_name"]=self.app_name
        session_value["dead_time"]=self.dead_time
	return json.dumps(session_value)

if __name__ == "__main__":
    session=Session(1,"Tom","ibridge",80)
    print session.getSessionStr()

