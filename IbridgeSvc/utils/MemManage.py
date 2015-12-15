#!/bin/bash

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

import memcache
import ConfigParser
from utils.Logger import *

#singleton
class MemMgmt(object):
    __instance=None
    __memClient=None
    def __new__(cls, *args, **kwargs):
	if not cls.__instance:
	    cls.__instance = super(MemMgmt, cls).__new__(cls, *args, **kwargs)
	    config = ConfigParser.ConfigParser()
	    config.readfp(open('/usr/ibridge/IbridgeSvc/conf/config.ini'))
	    host = config.get("Memcache","host")
	    port = config.get("Memcache","port")
	    cls.__memClient = memcache.Client([host+":"+port],debug=0)
	return cls.__instance
    
    def __init__(self):
	pass

    def get(self,key):
	value=MemMgmt.__memClient.get(key)
	return value

    def set(self,key,value):
	if value:
	    MemMgmt.__memClient.set(key,value)
	else:
	    MemMgmt.__memClient.delete(key)
    
if __name__=="__main__":
    mem=MemMgmt()
    print id(mem)
    mem.set('name','tom')
    print mem.get('name')
