#!/usr/bin/env python
#coding:utf8

import requests
import re


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


if __name__ == '__main__':
	urlsplit("http://www.1377.cc/Organization.aspx?id=34&du=12&c=wni"," --")