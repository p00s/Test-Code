#!/usr/bin/env python
#coding=utf-8

"""
for help http://www.yzqy.cc
这个模块主要用于对网页内容进行整理,将所有链接过滤出来插入数据库
"""
from bs4 import BeautifulSoup
import re
from sqlite3con import *
from request import opener

rule=r'[a-zA-z]+://[\w-]*[\.]?[\w]+\.[a-zA-Z]+'

def html(conn,url,body):
	soup = BeautifulSoup(body)
	links = soup.find_all('a')
	for link in links:
		_link=link.get('href')
		#print _link
		'''if str(re.findall(rule,_link)[0])!=url:
			print "err"
		else:	'''
		inser_data(conn,_link,TABLE_NAME_1)
	print "[info]insered!"


if __name__ == '__main__':
	header,body,bodysize,headersize,status=opener("http://www.yzqy.cc",'get',3)
	conn=init()
	html(conn,"http://www.yzqy.cc",body)