#!/usr/bin/env python
#coding=utf-8
"""
for help http://www.yzqy.cc
此模块为http请求模块,通过对比状态码,包返回大小来判断
"""

import requests

def opener(url,methed,times):
	'''通过传入的方法来请求网页'''
	if methed=='get':
		try:
			fopen=requests.get(url,timeout=times)
			header=fopen.headers
			body=fopen.content
			bodysize=len(body)
			headersize=len(str(header))
			status=fopen.status_code
			print "[info]currenting : "+url
			return header,body,bodysize,headersize,status
		except Exception, e:
			pass
	elif methed=='post':
		data={}
		fopen=requests.post(url,data,timeout=times)
	else:
		pass

	#print header,bodysize,status
	
	

'''if __name__ == '__main__':
	header,body,bodysize,headersize,status=opener("http://www.yzqy.cc",'get',2)
	print header'''