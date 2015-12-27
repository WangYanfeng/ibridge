#!/bin/python

class Bridge(object):

    def __init__(self,bridge_id):
	self.bridge_id=bridge_id
	self.bridge_no=None
	self.bridge_name=None
	self.management=None
	self.length=None
	self.height=None
	self.width=None
	self.over_date=None
        self.hole_num=None
        self.belong_user=None
        self.stake_id=None
        self.route=None
        self.description=None


    def setBridgeNo(self,bridge_no):
	self.bridge_no=bridge_no

    def setBridgeName(self,bridge_name):
	self.bridge_name=bridge_name

    def setManagement(self,management):
	self.management=management

    def setLength(self,length):
	self.length=length

    def setHeight(self,height):
	self.height=height

    def setWidth(self,width):
	self.width=width

    def setOverDate(self,over_date):
	self.over_date=over_date

    def setHoleNum(self,hole_num):
	self.hole_num=hole_num

    def setBelongUser(self,belong_user):
	self.belong_user=belong_user

    def setStakeId(self,stake_id):
	self.stake_id=stake_id

    def setRoute(self,route):
	self.route=route

    def setDescription(self,description):
	self.description=description

