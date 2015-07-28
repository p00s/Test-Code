#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
参数处理模块
"""
import sys,os

def banner():
	print "	________          _______    	__                            "
	print "|              |    |            |  |   |                          "
	print "|    ----------|    |   |--|   |  |   |                          "
	print "	-------|    |   |_ |   |  |   |                          "
	print "|--------      |    | ____     |  |   |_______                "
	print " \_________/              |__|  |__________|              "
	print "	   by:yzqycn http://www.yzqy.cc"

def helper():
	print "use: python sqlfinder.py [-o file] http://www.google.com/"

	

def argv_do():
	if len(sys.argv)<2:
		helper()
		os._exit(0)
	else:
		'''if sys.argv[1]=="-o":
			write=1'''
		return sys.argv[-1]
		




