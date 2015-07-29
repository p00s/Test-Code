#!/usr/bin/env python
#coding=utf-8

"""
for help http://www.yzqy.cc
这个模块主要用于对网页内容进行整理,将所有链接过滤出来插入数据库
"""
from bs4 import BeautifulSoup
import re
from sqlite3con import DB_method
import request

rule=r'[a-zA-z]+://[\w-]*[\.]?[\w]+\.[a-zA-Z]+'

class Spider(object):
	"""docstring for Spider"""
	def __init__(self):
		super(Spider, self).__init__()
		#self.arg = arg
		
	def html(self,url,body):
		soup = BeautifulSoup(body)
		links = soup.find_all('a')
		spider = DB_method()
		for i in links:
			link=i.get('href')
			#print _link
			'''if str(re.findall(rule,_link)[0])!=url:
				print "err"
				else:	'''
			spider.inser_data(link,spider.TABLE_NAME_1)
		print "[info]insered complied"
		return links
