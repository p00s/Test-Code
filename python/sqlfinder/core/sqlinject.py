#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
此模块为sql注入检测处理模块
"""

from  request import *

payload1="+and+1=1"
payload2="+and+1=2"
payload3="+'+"

def sqlinject(row,methed,timeout):
	pay1=str(row)+payload1
	pay2=str(row)+payload2
	pay3=str(row)+payload3
	_header,_body,_bodysize,_headersize,_status=opener(row,methed,timeout)
	header1,body1,bodysize1,headersize1,status1=opener(pay1,methed,timeout)
	header2,body2,bodysize2,headersize2,status2=opener(pay2,methed,timeout)
	header3,body3,bodysize3,headersize3,status3=opener(pay3,methed,timeout)
	print _status,status1,status2,status3
	if  _status != 404:
		print "[info]size1 : "+str(bodysize1)
		print "[info]size2 : "+str(bodysize2)
		print "[info]size3 : "+str(bodysize3)
		if bodysize1 != (bodysize2 or bodysize3):
			print "[info]issue :"+row
			return row
	else:
		print "[info]error status : ",status


