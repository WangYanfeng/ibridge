#!/bin/python

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

import web
from utils.Logger import *
from service.UserSvc import userSvc

class login:
    def GET(self):
        return 'haha'
    def POST(self):
        data = web.input()
        name=data.get('name')
        password=data.get('password')
	ibLogger.info("login user: %s",name)
	result = userSvc.checkPwd(name,password)
        if result:
	    web.redirect("/main.html")
	else:
	    web.redirect("/login.html")

