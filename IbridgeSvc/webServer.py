#!/usr/bin/python

import web
from action.login import login

urls=(
	'/ibridge/api/login','login',

)

app=web.application(urls,globals())
application=app.wsgifunc()

