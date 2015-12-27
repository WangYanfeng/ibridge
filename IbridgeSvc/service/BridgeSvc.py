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

class BridgeSvc(object):
    __dbMgmt = DBMgmt()
    __sessionMgmt = SessionMgmt()
    def __init__(self):
	pass

    def getBridge(self,bridge_id):
	sql = "select bridge_id,bridge_no,bridge_name,management,length,height,width,over_date,hole_num,stake_id,route,description,belong_user from bridge_info where bridge_id="+str(bridge_id)+";"
        results = BridgeSvc.__dbMgmt.execute(sql)
	if results and len(results) == 1:
	    re=results[0]
            bridge=Bridge(re[0])
	    bridge.setBridgeNo(re[1])
	    bridge.setBridgeName(re[2])
	    bridge.setManagement(re[3])
	    bridge.setLength(re[4])
	    bridge.setHeight(re[5])
	    bridge.setWidth(re[6])
	    bridge.setOverDate(re[7])
	    bridge.setHoleNum(re[8])
	    bridge.setStakeId(re[9])
	    bridge.setRoute(re[10])
	    bridge.setDescription(re[11])
	    bridge.setBelongUser(re[12])

            return bridge
	else:
	    ibLogger.info("bridge query error, multiple bridge_id:[%s]", bridge_id)
	return None

bridgeSvc=BridgeSvc()

if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=="getBridge":
	bridge=bridgeSvc.getBridge(1)
	print bridge
	print bridge.bridge_name
	print bridge.description

