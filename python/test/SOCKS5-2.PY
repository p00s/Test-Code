#!/usr/bin/env python
#coding:utf8

import socket
import struct
import argparse
import sys
import threading
import select
import Queue
import time

BUF_SIZE=4096
FLAG = 0
client_q=Queue.Queue()
server_q=Queue.Queue()


class Socks5proxy(object):

	def socks5server(self,sock,remote):
		try:
			inputs = [sock, remote]  
			while True:  
				r, w, e = select.select(inputs, [], [])  
				if sock in r:  
					if remote.send(sock.recv(BUF_SIZE)) <= 0:
						sock.close()
						remote.close()
						break
					#print "[*]client recv and send remote"  
				if remote in r:  
					if sock.send(remote.recv(BUF_SIZE)) <= 0:
						sock.close()
						remote.close()
						break 
					#print "[*]remote recv and send client"
					print "[*]current active :",threading.activeCount()  
		#except Exception,e:
		#	print e
		except KeyboardInterrupt:
			remote.close()
			sock.close()
			sys.exit(1)
			
	def remote(self,ipaddr,port,mode,c):#forward client request
		global FLAG
		try:
			r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			r.settimeout(15)
			r.connect((ipaddr, port))
			if mode==1:#tcp type
				reply = b"\x05\x00\x00\x01"
				FLAG = 1
				print "[*]Connect remote success ",ipaddr,port
			else:#udp not suport
				reply = b"\x05\x07\x00\x01" #
				FLAG = 0
			local = r.getsockname()
			reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
		except Exception, e:
			print e
			reply = b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
			FLAG = 0
			print "[*]connect remote fail ",ipaddr,port
		c.send(reply)
		return r

	def lsocks5(self,port):#local socks5 server mode
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(("0.0.0.0", port))
			s.listen(10)
			print "[*]Socks5 server start on 0.0.0.0:",port
			while True:
				c,address = s.accept()
				print "[*]Client from :",address[0],address[1]
				c.recv(BUF_SIZE)
				c.send(b"\x05\x00")
				data = c.recv(BUF_SIZE)
				mode = ord(data[1])  
				addrtype = ord(data[3])
				if addrtype == 1:       # IPv4  
					addr = socket.inet_ntoa(data[4:8])
					port = (struct.unpack('!H', data[8:]))[0]  
				elif addrtype == 3:     # Domain name 
					length = struct.unpack('B', data[4:5])[0]
					addr = data[5:5 + length]
					port = (struct.unpack('!H', data[5 + length:]))[0]
				print "[*]Connect ",addr,port
				r = self.remote(addr,port,mode,c)
				print "[*]remote invoke success!"
				if FLAG:
					#self.socks5server(c,r)
					threading.Thread(target=self.socks5server, args=(r,c)).start()
					#threading.Thread(target=self.socks5server_server, args=(r,c)).start()
		except Exception,e:
			print e
			#print "[*]Sockes5 server start fail..."

	def rsocks5(self,daddr,dport):
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((daddr,dport))
			print "[*]Connected to remote :", daddr,dport
			while True:
				s.recv(BUF_SIZE)
				print 1
				s.send(b"\x05\x00")
				data = s.recv(BUF_SIZE)
				mode = ord(data[1])  
				addrtype = ord(data[3])
				print 2  
				if addrtype == 1:       # IPv4  
					addr = socket.inet_ntoa(data[4:8])
					port = (struct.unpack('!H', data[8:]))[0]  
				elif addrtype == 3:     # Domain name  
					length = struct.unpack('B', data[4:5])[0]
					addr = data[5:5 + length]
					port = (struct.unpack('!H', data[5 + length:]))[0]
				print addr,port
				r = self.remote(addr,port,mode,s)#forward requests
				print "[*]remote invoke success!"
				if FLAG:
					#self.socks5server(s,r)
					print "[*]start ......"
					threading.Thread(target=self.socks5server, args=(s,r)).start()
					#threading.Thread(target=self.socks5server_server, args=(r,s)).start()

		except Exception,e:
			print e
			#print "[*]Remote listener port closed..."
			sys.exit(1)

	def forward(self,ports):#forward mode
		global BUF_SIZE

		def translate(s,c):
			print "hehe2"
			while True:
				conlist =[c,s]
				r, w, e = select.select(conlist,[],[])
				print "hehe3"
				if c in r:
					print "hehe4"
					if s.send(c.recv(BUF_SIZE)) <=0:
						#c2.close()
						break
					print "client recv and send remote"
				if s in r:
					print "hehe5"
					if c2.send(c1.recv(BUF_SIZE)) <=0:
						#c1.close()
						break
					print "remote recv and send client"
					print "[*]current active :",threading.activeCount()  
	
		try:
			sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 1
			sock_1.bind(("0.0.0.0", ports[0]))
			sock_1.listen(100)
			print "[*]Listen on 0.0.0.0:",ports[0]

			sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 2
			sock_2.bind(("0.0.0.0", ports[1]))
			sock_2.listen(100)
			print "[*]Listen on 0.0.0.0:",ports[1]

			inputs = [sock_1,sock_2]
			con =[]
			while True:
				rs, ws, es = select.select(inputs,[],[])
				if sock_1 in rs:
					c1, address1 = sock_1.accept()
					print "[*]Client from :"+str(address1[0])+" :"+str(address1[1])+" on Port "+str(ports[0])
					con.append(c1)
				if sock_2 in rs:
					while True:
						c2, address2 = sock_2.accept()
						print "[*]Client from :"+str(address2[0])+" :"+str(address2[1])+" on Port "+str(ports[1])
						if c1 in con:
							print "hehe"
							threading.Thread(target=translate, args=(c1,c2)).start()
							#con.append(c2)



				'''conn1,address1 = sock_1.accept()
				print "[*]Client from :"+str(address1[0])+" :"+str(address1[1])+" on Port "+str(ports[0])
				conn2,address2 = sock_2.accept()
				print "[*]Client from :"+str(address2[0])+" :"+str(address2[1])+" on Port "+str(ports[1])'''

			#threading.Thread(target=sockclient, args=(ports)).start()
			#threading.Thread(target=sockserver, args=(ports)).start()

		except Exception, e:
			print e


def main():
	try:

		parser = argparse.ArgumentParser(prog='Tsocks', 
							description='Tsocks v1.0', 
							formatter_class=argparse.ArgumentDefaultsHelpFormatter,
							usage='''%(prog)s [options]
	Tsocks -s -p 1028	Socks5 server mode
	Tsocks -s -r 1.1.1.1 -p 8001	Reverse socks5 server mode
	Tsocks -f 8001 8002	Port forward mode''',
							 )
		parser.add_argument('-s','--server', action="store_true", default=False,help='Socks5 server mode')
		parser.add_argument('-p','--port',metavar="PORT", dest='port', type=int, default=1080,help='Socks5 server mode listen port or remote port')
		parser.add_argument('-r','--remote',metavar="REMOTE IP", type=str, default=None,help='Reverse socks5 server mode ,set remote relay IP')  
		parser.add_argument('-f','--forward',nargs=2, metavar=('PORT1', 'PORT2'),default=(None),type=int,help='Set forward mode,and listen ports')  
		args = parser.parse_args()
		if len(sys.argv) == 1:
			parser.print_help()
			sys.exit(1)
		elif (args.server and args.forward):
			print "[-]Socks5 or forward mode only one..."
			sys.exit(1)

		if args.server:
			if args.remote:
				resocks5 = Socks5proxy()
				resocks5.rsocks5(args.remote,args.port)
			else:
				losocks5 = Socks5proxy()
				losocks5.lsocks5(args.port)
		elif args.forward:
				lforward = Socks5proxy()
				lforward.forward(args.forward)
	except Exception,e:
		print e
	#except KeyboardInterrupt:
		#sys.exit(1)
	#finally KeyboardInterrupt:
	#	sys.exit(1)




if __name__ == '__main__':
	main()
