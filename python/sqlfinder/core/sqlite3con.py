#!/usr/bin/env python
#coding=utf-8

"""
for help http://www.yzqy.cc
这个模块主要用于sqlite3的数据库连接和操作方法
"""

import sqlite3

class DB_method(object):
	"""docstring for DB_method"""		
	#global var
	DB_FILE_PATH = 'data/sqlfinder.db'  
	#database path
	TABLE_NAME_1 = 'spider'
	TABLE_NAME_2 = 'sqlinject'
	#table name
	def __init__(self):
		#self.arg = arg
		self.conn=self.get_conn(self.DB_FILE_PATH)
		self.cu = self.get_cursor(self.conn)

	def get_conn(self,path):
	 	'''连接sqlite3数据库方法'''
	 	try:  
	        		return sqlite3.connect(path)  
	        		print "connect sussess"
	    	except sqlite3.Error,e:  
	        		print "connect sqlite3 database fail!", "\n", e.args[0]  
        
	def get_cursor(self,conn):
		'''获取游标'''
		if conn is not None:
			return conn.cursor()
		else:
			return get_conn(DB_FILE_PATH) .get_cursor()

	def drop_table(self):
		'''判断是否有数据库存在,有就删除'''
		sql = 'DROP TABLE IF EXISTS %s' % self.TABLE_NAME_1
		sql1='DROP TABLE IF EXISTS %s' % self.TABLE_NAME_2
 		self.cu.execute(sql)
 		self.cu.execute(sql1)
 		self.conn.commit()
 		print "[info]drop sussess"

	def create_table(self):
 		'''创建新数据库方法'''
 		sql = 'CREATE TABLE %s(id INTEGER PRIMARY KEY ,link VARCHAR,methed VARCHAR,data VARCHAR)' % self.TABLE_NAME_1
 		sql1='CREATE TABLE %s(id INTEGER PRIMARY KEY ,link VARCHAR,methed VARCHAR,data VARCHAR)' % self.TABLE_NAME_2
 		self.cu.execute(sql)
 		self.cu.execute(sql1)
 		self.conn.commit()
 		print "[info]create sussess"

	def inser_data(self,data,table):
	 	'''插入数据方法'''
	 	if data is not None:
	 		sql='INSERT INTO %s(link) VALUES("%s")' % (table,data)
	 		#cu=self.get_cursor(conn)
	 		self.cu.execute(sql)
	 		self.conn.commit()
	 	#print "[info]inser success  "+table

	def select_data(self,table):
		'''查询方法'''
		sql='SELECT link FROM %s' % table
		#cu=self.get_cursor(conn)
		res= self.cu.fetchall(sql)
		self.conn.commit()
		print "[info]select success "
		return res

	def __del__(self):
		return self.conn.close()

