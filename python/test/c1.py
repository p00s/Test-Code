#!/usr/bin/env python
#coding:utf8

class Ren:
	name="zhangsan"
	high = 181
	width = 50
	__money = "i have 100 doc"

	def run(self):
		print "I am running"
	def say(self):
		print "i love you"
	def __lie(self):
		print "hehehehhe i am lie"
	def get(self):
		return self.__lie()
		print __money

if __name__ == '__main__':
	zhangsan = Ren()
	zhangsan.name = "lisi"
	zhangsan.money = "100000"
	zhangsan.say
	zhangsan.run 
	zhangsan.get
