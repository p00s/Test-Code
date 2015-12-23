#!/usr/bin/env python
#coding:utf8

import socket
import struct
import argparse
import sys
import threading
import Queue

BUF_SIZE=4096
FLAG = 0
client_q=Queue.Queue()
server_q=Queue.Queue()
CON_C =None
CON_S =None


class Socks5proxy(object):

	def socks5server_client(self,r,c):
		try:
			while True:
				#r.send(c.recv(BUF_SIZE))
				if r.send(c.recv(BUF_SIZE)) <= 0:
					r.close()
					c.close()
					break 
		except KeyboardInterrupt:
			r.close()
			c.close()
			sys.exit(1)

	def socks5server_server(self,r,c):
		try:
			while True:
				if c.send(r.recv(BUF_SIZE)) <= 0:
					r.close()
					c.close()
					break  
		except KeyboardInterrupt:
			r.close()
			c.close()
			sys.exit(1)

			#if r.send(c.recv(BUF_SIZE)) <= 0:
			#	break 
			#if c.send(r.recv(BUF_SIZE)) <= 0:
			#	break  
			
	def remote(self,ipaddr,port,mode,c):#forward client request
		global FLAG
		try:
			r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			r.connect((ipaddr, port))
			if mode==1:#tcp type
				reply = b"\x05\x00\x00\x01"
				FLAG = 1
				print 55
			else:#udp not suport
				reply = b"\x05\x07\x00\x01" #
				FLAG = 0
			print 6
			local = r.getsockname()
			reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
		except Exception, e:
			reply = b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
			FLAG = 0
		print 777
		c.send(reply)
		return r

	def lsocks5(self,port):#local socks5 server mode
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(("0.0.0.0", port))
			s.listen(1000)
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
				print addr,port
				r = self.remote(addr,port,mode,c)
				print 5
				if FLAG:
					#self.socks5server(r,c)
					threading.Thread(target=self.socks5server_client, args=(r,c)).start()
					threading.Thread(target=self.socks5server_server, args=(r,c)).start()
		except Exception,e:
			print e
			#print "[*]Sockes5 server start fail..."
			sys.exit(1)

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
				if FLAG:
					threading.Thread(target=self.socks5server_client, args=(r,s)).start()
					threading.Thread(target=self.socks5server_server, args=(r,s)).start()

		except Exception,e:
			print e
			#print "[*]Remote listener port closed..."
			sys.exit(1)

	def forward(self,ports):#forward mode
		global BUF_SIZE
		global CON_C
		global CON_S
		global client_q
		global server_q

		def sockclient(*port):
			try:
				
				sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 2
				sock_1.bind(("0.0.0.0", port[1]))
				sock_1.listen(100)
				print "[*]Listen on 0.0.0.0:",port[1]

				while True:
					conn1,address1 = sock_1.accept()
					print "[*]Client from :"+str(address1[0])+" :"+str(address1[1])+" on Port "+str(port[1])
					while True:
						client_q.put(conn1.recv(BUF_SIZE))
						conn1.send(server_q.get())
			except KeyboardInterrupt:
				sys.exit(1)

		def sockserver(*port):
			global client_q
			global server_q
			try:
				sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 1
				sock_2.bind(("0.0.0.0", port[0]))
				sock_2.listen(100)
				print "[*]Listen on 0.0.0.0:",port[0]
				while True:
					conn2,address2 = sock_2.accept()
					CON_C =conn2
					print "[*]Client from :"+str(address2[0])+" :"+str(address2[1])+" on Port "+str(port[0])
					while True:
						conn2.send(client_q.get())
						server_q.put(conn2.recv(BUF_SIZE))
			except KeyboardInterrupt:
				sys.exit(1)
		

		try:
			'''sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 1
			sock_1.bind(("0.0.0.0", ports[0]))
			sock_1.listen(5)
			print "[*]Listen on 0.0.0.0:",ports[0]

			sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 1
			sock_2.bind(("0.0.0.0", ports[1]))
			sock_2.listen(5)
			print "[*]Listen on 0.0.0.0:",ports[1]

			while True:
				conn1,address1 = sock_1.accept()
				print "[*]Client from :"+str(address1[0])+" :"+str(address1[1])+" on Port "+str(ports[0])
				conn2,address2 = sock_2.accept()
				print "[*]Client from :"+str(address2[0])+" :"+str(address2[1])+" on Port "+str(ports[1])'''

			threading.Thread(target=sockclient, args=(ports)).start()
			threading.Thread(target=sockserver, args=(ports)).start()

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
