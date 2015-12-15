#!/bin/python

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/utils/")

from DBManage import DBMgmt

class UserSvc(object):
    dbMgmt = DBMgmt()

    def __init__(self):
	pass

    def checkPwd(self, name, passwd):
	sql = "select * from user where name='"+name+"' and password='"+passwd+"';"
	results = UserSvc.dbMgmt.execute(sql)
	if results:
	    return True
	else :
	    return False

userSvc = UserSvc()

if __name__=="__main__":
    result=userSvc.checkPwd("tom","123")
    print result
