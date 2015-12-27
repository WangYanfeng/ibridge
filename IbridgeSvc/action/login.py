#!/bin/python

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")
#os.path.dirname(os.path.realpath(__file__))

import web
from utils.Logger import *
from utils.decorate import *
from service.UserSvc import userSvc

render = web.template.render('/usr/ibridge/UI/frontend/')

class login:
    def GET(self,**kwargs):
	return render.login()

    def POST(self,**kwargs):
        data = web.input()
        user_name=data.get('name')
        password=data.get('password')
	session = userSvc.login(user_name,password)
        
        if session:
	    web.header("Content-Type","text/html;charset=UTF-8;")
	    web.setcookie("session_id",session.getSessionId(),90)
	    web.setcookie("user_name",user_name,90)
	    web.redirect("/ibridge/bridge/"+str(session.getUserId()))
	else:
	    return render.login()

