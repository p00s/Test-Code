#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
此模块为http请求模块,通过对比状态码,包返回大小来判断
"""

import requests

class Myhttp(object):
	"""docstring for Myhttp"""
	def __init__(self):
		super(Myhttp, self).__init__()

	def opener(self,url,method,times):
		'''通过传入的方法来请求网页'''
		if method=='get':
			try:	
				fopen=requests.get(url,timeout=times)
				body=fopen.content
				bodysize=len(body)
				status=fopen.status_code
				print "[info]currenting : "+fopen.url
				return body,bodysize,status
			except Exception, e:
				print e 
				return self.opener(url,method,times)
		elif method=='post':
			data={}
			fopen=requests.post(url,data,timeout=times)
		else:
			pass

		



