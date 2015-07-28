#!/usr/bin/env python
#coding=utf-8

"""
for help http://www.yzqy.cc
这个模块主要用于sqlite3的数据库连接和操作方法
"""

import sqlite3

#global var
DB_FILE_PATH = 'data/sqlfinder.db'  
#database path

TABLE_NAME_1 = 'spider'
TABLE_NAME_2 = 'sqlinject'
#table name

def get_conn(path):
 	'''连接sqlite3数据库方法'''
 	try:  
        		return sqlite3.connect(path)  
        		print "connect sussess"
    	except sqlite3.Error,e:  
        		print "connect sqlite3 database fail!", "\n", e.args[0]  
        	

def get_cursor(conn):
	'''获取游标'''
	'''if conn is not None:'''
	cu=conn.cursor()
	return cu
	'''else:
		return get_conn(DB_FILE_PATH) .cursor()'''

def drop_table(conn,table1,table2):
	'''判断是否有数据库存在,有就删除'''
	sql = 'DROP TABLE IF EXISTS %s' % table1
	sql1='DROP TABLE IF EXISTS %s' % table2
	cu = get_cursor(conn)
 	cu.execute(sql)
 	cu.execute(sql1)
 	conn.commit()
 	print "[info]drop sussess"

def create_table(conn,table1,table2):
 	'''创建新数据库方法'''
 	sql = 'CREATE TABLE %s(id INTEGER PRIMARY KEY ,link VARCHAR,methed VARCHAR,data VARCHAR)' % table1
 	sql1='CREATE TABLE %s(id INTEGER PRIMARY KEY ,link VARCHAR,methed VARCHAR,data VARCHAR)' % table2
 	cu = get_cursor(conn)
 	cu.execute(sql)
 	cu.execute(sql1)
 	conn.commit()
 	print "[info]create sussess"

def inser_data(conn,data,table):
 	'''插入数据方法'''
 	if data is not None:
 		sql='INSERT INTO %s(link) VALUES("%s")' % (table,data)
 		cu=get_cursor(conn)
 		cu.execute(sql)
 		conn.commit()
 	#print "[info]inser success  "+table

def select_data(conn,table):
	'''查询方法'''
	sql='SELECT link FROM %s' % table
	cu=get_cursor(conn)
	cu.execute(sql)
	conn.commit()
	res= cu.fetchall()
	print "[info]select success "
	return res

def init():
	'''初始化方法'''
	conn=get_conn(DB_FILE_PATH)
	drop_table(conn,TABLE_NAME_1,TABLE_NAME_2)
	create_table(conn,TABLE_NAME_1,TABLE_NAME_2)
	print "[info] init sussessful"
	return conn




if __name__ == '__main__':
	init()