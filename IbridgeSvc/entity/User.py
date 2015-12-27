#!/bin/python

class User(object):
    def __init__(self,user_id,user_name):
	self.user_id = user_id
	self.user_name = user_name
	self.bridges = None

    def getUserId(self):
	return self.user_id
    
    def getUserName(self):
	return self.user_name

    def getBridge(self):
	return self.bridges

    def setUserName(self,user_name):
	self.user_name=user_name

    def setUserId(self,user_id):
	self.user_id=user_id

    def setBridges(self,bridges):
	self.bridges=bridges


if __name__ == "__main__":
    user=User(1,"Tom")
    print user.getUserName()
