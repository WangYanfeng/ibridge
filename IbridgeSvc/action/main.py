#!/bin/python

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

import web
from utils.Logger import *
from utils.decorate import *
from entity.User import User
from service.UserSvc import userSvc
from service.BridgeSvc import bridgeSvc

render = web.template.render('/usr/ibridge/UI/frontend/')

class main:
    def GET(self,bridge_id):
	session_id=web.cookies().get("session_id")
	user_name=web.cookies().get("user_name")
	session=userSvc.checkSession(session_id, user_name)
	if session:
	    web.header("Content-Type","text/html;charset=UTF-8;")
            web.setcookie("session_id",session_id,90)
            web.setcookie("user_name",user_name,90)
	    user=User(session.getUserId(),session.getUserName())
	    bridge=bridgeSvc.getBridge(bridge_id)
            return render.main(user,bridge)
	else:
	    return render.login()

