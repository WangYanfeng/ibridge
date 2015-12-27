#!/bin/python
# encoding=utf-8

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

reload(sys)
sys.setdefaultencoding('utf8')

import json
from entity.User import User
from entity.Bridge import Bridge
from utils.SessionMgmt import *
from utils.Logger import *
from utils.DBManage import DBMgmt

class UserSvc(object):
    __dbMgmt = DBMgmt()
    __sessionMgmt = SessionMgmt()

    def __init__(self):
	pass

    def checkPwd(self, name, passwd):
	if name and passwd:
	    sql = "select * from user where name='"+name+"' and password='"+passwd+"';"
	    results = UserSvc.__dbMgmt.execute(sql)
	    if len(results) == 1:
	    	return results[0]
	    else :
	    	ibLogger.info("user login error, multiple name:[%s]", name)
	    	return False

    def login(self, name, passwd):
	user = self.checkPwd(name,passwd)
	session_id=None
	if user[0]:
	    session = UserSvc.__sessionMgmt.saveSession(name,user[0])
	    ibLogger.info("user login success: [%s]", name)
	return session

    def checkSession(self, session_id, user_name):
	result = UserSvc.__sessionMgmt.checkSession(session_id,user_name)
	return result

    def getBelongedBridges(self, user_id):
	sql = "select bridge_id,bridge_no,bridge_name,belong_user from bridge_info where belong_user="+str(user_id)+";"
	results = UserSvc.__dbMgmt.execute(sql)
	bridges_list=[]
	for re in results:
	    bridge=Bridge(re[0])
	    bridge.setBridgeNo(re[1])
	    bridge.setBridgeName(re[2])
	    bridge.setBelongUser(re[3])
	    bridges_list.append(bridge)
	return bridges_list

userSvc = UserSvc()

if __name__=="__main__":
    result=userSvc.getBelongedBridges(1)
    print result[0].width
