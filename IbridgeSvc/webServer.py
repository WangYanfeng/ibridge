#!/usr/bin/python

import web
from action.login import login
from action.main import main
from action.bridge import bridge

urls=(
	'/ibridge/login','login',
	'/ibridge/bridge/(.+)','bridge',
	'/ibridge/main/(.+)','main'
)

app=web.application(urls,globals())
application=app.wsgifunc()

