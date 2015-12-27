#!/bin/python

import sys
sys.path.append("/usr/ibridge/IbridgeSvc/")

import MySQLdb
import ConfigParser
from utils.Logger import *

class DBMgmt(object):
    __instance=None
    __connection=None
    def __new__(cls, *args, **kwargs):
	if not cls.__instance:
	    cls.__instance = super(DBMgmt,cls).__new__(cls,*args,**kwargs)

	return cls.__instance

    def __init__(self):
	try:
	    config = ConfigParser.ConfigParser()
	    config.readfp(open('/usr/ibridge/IbridgeSvc/conf/config.ini'))
	    self.host = config.get("MysqlDB","host")
	    self.user = config.get("MysqlDB","user")
	    self.port = config.get("MysqlDB","port")
	    self.passwd = config.get("MysqlDB","password")
	    self.dbname = config.get("MysqlDB","dbname")
	    DBMgmt.__connection = MySQLdb.Connect(host=self.host,user=self.user,passwd=self.passwd,port=int(self.port),charset="gb2312")
	    DBMgmt.__connection.select_db(self.dbname)
	except MySQLdb.Error,e:
	    ibLogger.error("MySQLDB connection error - [%s]",e)

    def execute(self, sql, count=None):
	try:
	    DBMgmt.__connection.ping()
	except Exception,e:
	    ibLogger.error("MySQLDB connection has closed - create new connection")
	    DBMgmt.__connection=MySQLdb.Connect(host=self.host,user=self.user,passwd=self.passwd,port=int(self.port))
	    DBMgmt.__connection.select_db(self.dbname)

	try:
	    ibLogger.info("MySQLDB execute sql - [%s]",sql)
	    cur=DBMgmt.__connection.cursor()
	    cur.execute(sql)
	    results=None
	    if not count:
		results=cur.fetchall()
	    else:
		results=cur.fetchmany(count)
	    DBMgmt.__connection.commit()
	    cur.close()
	    #DBMgmt.__connection.close()
	    return results
	except MySQLdb.Error,e:
	    ibLogger.error("MySQLDB execute error - [%s]",e)
 
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
    	mgmt=DBMgmt()
    	print id(mgmt)
    	results=mgmt.execute(sql="select * from user where name='Tom' and password='123'") 
    	print results
