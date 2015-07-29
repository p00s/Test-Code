#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
主要模块,调动其他模块进行工作
"""

from core.args import *
from core.sqlite3con import *
from core.request import Myhttp
from core.spider import *
from core.sqlinject import *
import os

#下面是程序配置参数
threads=5
timeout=10
deep=5
flag = 0

def main():
	#write=0
	banner()
	#初始化
	url=argv_do()
	#参数处理
	initdb =  DB_method()
	initdb.drop_table()
	initdb.create_table()
	#初始化数据库
	first_open = Myhttp()
	get_body,get_bodysize,get_status=first_open.opener(url,'get',timeout)
	#打开第一个根页面
	first_spider = Spider()
	print "[info]first spider"
	root_links = first_spider.html(url,get_body)
	#进行第一次url解析,将解析出来的url存入数据库
	#first_select = DB_method()
	#res=first_select.select_data(first_select.TABLE_NAME_1)
	#第一次取出数据
	deep_open = Myhttp()
	deep_spider = Spider()

	def tree(links):
		global threads
		global timeout
		global flag
		global deep
		flag =flag+1
		print "[info] begin deep spider"
		for row in links:
			'''while  threading.active_count() < thread:
			sp=threading.Thread(target=work,args=([row,]))
			sp.start()
			sp.join()
			def work(row):
			mylock.acquire()'''
			try:	
				print "[info] rowing :",row
				deep_body,deep_bodysize,deep_status = deep_open.opener(row,'get',timeout)
				tree_links = deep_spider.html(row,deep_body)
				'''while flag <= deep:
					return tree(tree_links)'''
			except Exception, e:
				pass
			#mylock.release()

			
	#mylock = threading.RLock()
	tree(root_links)

	first_select = DB_method()
	res=first_select.select_data(first_select.TABLE_NAME_1)
	deep_test = Sqlinject()
	for r in res:
		issues=deep_test.sqltest(r,'get',timeout,threads)
		first_select.inser_data(issues,first_select.TABLE_NAME_2)

if __name__ == '__main__':
	main()
