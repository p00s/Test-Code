#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
主要模块,调动其他模块进行工作
"""

from core.args import *
from core.sqlite3con import *
from core.request import *
from core.spider import *
from core.sqlinject import *
import os

#下面是程序配置参数
threads=1
timeout=10
deep=10


def main():
	#write=0
	banner()
	url=argv_do() 
	conn=init()
	get_header,get_body,get_bodysize,get_headersize,get_status=opener(url,'get',timeout)
	html(conn,url,get_body)
	res=select_data(conn,TABLE_NAME_1)
	for row in res:
		issues=sqlinject(row[0],'get',timeout)
		inser_data(conn,issues,TABLE_NAME_2)

if __name__ == '__main__':
	main()
