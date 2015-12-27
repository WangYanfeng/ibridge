#!/bin/python
# encoding=utf8

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

reload(sys)
sys.setdefaultencoding('utf8')

import web
from utils.Logger import *
from utils.decorate import *
from entity.User import User
from service.UserSvc import userSvc

render = web.template.render('/usr/ibridge/UI/frontend/')

class bridge:
    def GET(self,user_id):
	session_id=web.cookies().get("session_id")
	user_name=web.cookies().get("user_name")
	session=userSvc.checkSession(session_id, user_name)
	if session:
	    web.header("Content-Type","text/html;charset=UTF-8;")
            web.setcookie("session_id",session_id,900)
            web.setcookie("user_name",user_name,900)
	    user=User(session.getUserId(),session.getUserName())
	    bridges=userSvc.getBelongedBridges(session.getUserId())
            return render.bridge(user,bridges)
	else:
	    return render.login()

