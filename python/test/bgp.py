#!/usr/bin/env python
#coding:utf8
'''
作者:YZQYCN
博客:http://www.yzqy.cc
'''

import requests
import sys,os
from bs4 import BeautifulSoup
import time
import socket

class Main(object):
	refile = 'bgp.txt'
	def __init__(self,argv):
		if len(argv) < 2:
			print "Mast give a domain or ip"
			os._exit(0)
		try:
			self.root=socket.gethostbyname(argv[1])
		except Exception, e:
			print  e
			os._exit(0)
		if os.path.isfile(self.refile):
			os.remove(self.refile)
	def run(self):
		#请求网页内容
		headers={
			'Host': 'bgp.he.net',

			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',

			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate',
			'Cookie': '_bgp_session=BAh7BzoPc2Vzc2lvbl9pZEkiJTMxMWMwOTAxN2MxNzBkZTQ4ZDNjZTcyNmU2ZDU2MTMyBjoGRUY6EF9jc3JmX3Rva2VuSSIxWmtMYWZsaFVFa1RMbmJ1N3pHM1pnWVhxcmpBekw2U0Q5TUlXeXFpbWJ3VT0GOwZG--31cda14f2b0e1bfac2e1dc5b1e9a08fb917eae52; __utma=83743493.1604930050.1438048038.1438048038.1438048038.1; __utmb=83743493.1.10.1438048038; __utmc=83743493; __utmz=83743493.1438048038.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
			'Connection': 'keep-alive',
			'If-None-Match': '069e127dd5a04e3d410bbf99db87de14-gzip',
			'Cache-Control': 'max-age=0'
			}
		try:			
			fo=requests.get('http://bgp.he.net/ip/'+self.root,headers=headers)
			return	fo.content
		except Exception, e:
			print e
			os._exit(0)

	def html(self,body):
		#提取获得的链接
		soup = BeautifulSoup(body)
		dns = soup.find('div',id = 'dns')
		links = dns.find_all('a')
		fo = open(self.refile,'a+')
		for i in links:
			print " "+i.get('href').replace('/dns/','')
			fo.writelines(i.get('href').replace('/dns/','') + '\n')	
		fo.close()
		print "一共找到了"+str(len(links)) +"条内容,结果已经存于本目录的refile.txt文件中!"

if __name__ == '__main__':
	try:
		os.system("clear")
	except Exception, e:
		os.system("cls")
	print '''
	 Use: python  bgp.py  < ip or domain>
	             http://www.yzqy.cc'''
	print "----------------------------------------------------------------"
	try:
		my = Main(sys.argv)
		content = my.run()
		my.html(content)
	except KeyboardInterrupt:
		print " over!"
		os._exit(0)
	
