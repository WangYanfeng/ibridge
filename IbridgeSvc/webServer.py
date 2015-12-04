#!/usr/bin/python

import web

urls=('/ibridge/index','index')

class index:  
    def GET(self):
    	return 'Hello Web.py!'
app=web.application(urls,globals())
application=app.wsgifunc()
