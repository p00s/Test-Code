#!/usr/bin/env python
#coding:utf8

import socket
import struct
import argparse
import sys
import threading
import select


BUF_SIZE=4096
FLAG = 0
CMD = "ok"


class Socks5proxy(object):

	def exchange_data(self,sock,remote):#forward data
		try:
			inputs = [sock, remote]  
			while True:  
				r, w, e = select.select(inputs, [], [])  
				if sock in r:  
					if remote.send(sock.recv(BUF_SIZE)) <= 0:
						sock.close()
						remote.close()
						break
				if remote in r:  
					if sock.send(remote.recv(BUF_SIZE)) <= 0:
						sock.close()
						remote.close()
						break 
					#print "[*]current active :",threading.activeCount()  
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
				#Connect remote success 
			else:#udp not suport
				reply = b"\x05\x07\x00\x01" #
				FLAG = 0
			local = r.getsockname()
			reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
		except Exception, e:
			print e
			reply = b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
			FLAG = 0
			#connect remote fail
		c.send(reply)
		return r

	def local_socks5(self,port):#local socks5 server mode
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(("0.0.0.0", port))
			s.listen(100)
			print "[*]Socks5 server start on 0.0.0.0:",port
			while True:
				c,address = s.accept()
				print "[*]Client from :",address[0],address[1]
				c.recv(BUF_SIZE)
				c.send(b"\x05\x00")
				data = c.recv(BUF_SIZE)
				if not data:
					c.shutdown(socket.SHUT_RDWR)
					c.close()
					continue
				mode = ord(data[1])  
				addrtype = ord(data[3])
				if addrtype == 1:       # IPv4  
					addr = socket.inet_ntoa(data[4:8])
					port = (struct.unpack('!H', data[8:]))[0]  
				elif addrtype == 3:     # Domain name 
					length = struct.unpack('B', data[4:5])[0]
					addr = data[5:5 + length]
					port = (struct.unpack('!H', data[5 + length:]))[0]
				#print "[*]Connect ",addr,port
				r = self.remote(addr,port,mode,c)
				if FLAG:
					threading.Thread(target=self.exchange_data, args=(r,c)).start()
		except Exception,e:
			print e
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			print "[*]Sockes5 server start fail..."

	def reverse_socks5_main(self,daddr,dport):#reverse socks5 mode main
		global BUF_SIZE
		global FLAG
		global CMD

		try:
			print daddr,dport
			s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s1.connect((daddr,dport))
			print "[*]Connected to remote :", daddr,dport
			while True:#loop and recv forward server send a cmd and product a new socket to do with socks5 proxy
				flag =s1.recv(BUF_SIZE)
				if flag==CMD:
					threading.Thread(target=self.reverse_socks5_hand,args=(daddr,dport)).start()
		except Exception,e:
			#print e
			print "[*]Remote listener port closed..."
			s1.shutdown(socket.SHUT_RDWR)
			s1.close()

	def reverse_socks5_hand(self,daddr,dport):#reverse socks5 mode handsheak
		try:
			s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s2.connect((daddr,dport))
			s2.recv(BUF_SIZE)	
			s2.send(b"\x05\x00")
			data = s2.recv(BUF_SIZE)
			if data:
				mode = ord(data[1])  
				addrtype = ord(data[3]) 
				if addrtype == 1:       # IPv4  
					addr = socket.inet_ntoa(data[4:8])
					port = (struct.unpack('!H', data[8:]))[0]  
				elif addrtype == 3:     # Domain name  
					length = struct.unpack('B', data[4:5])[0]
					addr = data[5:5 + length]
					port = (struct.unpack('!H', data[5 + length:]))[0]
				#print addr,port
				r = self.remote(addr,port,mode,s2)#forward requests
				self.exchange_data(s2,r)
			else:								
				s2.shutdown(socket.SHUT_RDWR)
				s2.close()
		except Exception,e:
			print e
			s2.shutdown(socket.SHUT_RDWR)
			s2.close()

	def forward_translate(self,s,c):#port data exchange
		global BUF_SIZE
		try:
			conlist =[c,s]
			while True:
				r, w, e = select.select(conlist,[],[])
				if c in r:
					if s.send(c.recv(BUF_SIZE)) <=0:
						c.shutdown(socket.SHUT_RDWR)
						c.close()
						s.shutdown(socket.SHUT_RDWR)
						s.close()
						break
				if s in r:
					if c.send(s.recv(BUF_SIZE)) <=0:
						s.shutdown(socket.SHUT_RDWR)
						s.close()
						c.shutdown(socket.SHUT_RDWR)
						c.close()
						break
					#print "[*]current active :",threading.activeCount()
		except Exception,e:
			raise e
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			c.shutdown(socket.SHUT_RDWR)
			c.close()

	def forward_main(self,ports):#forward mode
		global BUF_SIZE
		global CMD

		try:
			sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #listen on port1 socks5 server rev
			sock_s.bind(("0.0.0.0", ports[0]))
			sock_s.listen(100)
			print "[*]Listen on 0.0.0.0:",ports[0]

			sock_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 2
			sock_c.bind(("0.0.0.0", ports[1]))
			sock_c.listen(100)
			print "[*]Listen on 0.0.0.0:",ports[1]

			inputs = [sock_s,sock_c]
			con_cmd =None

			while True:#Asynchronous I/O
				rs, ws, es = select.select(inputs,[],[])
				if sock_s in rs:
					if not con_cmd:#accept server reverse socket as cmd socket,if client has new connect,tell cmd socket
						con_s, address1 = sock_s.accept()
						print "[*]Client from :"+str(address1[0])+" :"+str(address1[1])+" on Port "+str(ports[0])
						con_cmd =con_s

				if sock_c in rs:
					con_c, address2 = sock_c.accept()
					print "[*]Client from :"+str(address2[0])+" :"+str(address2[1])+" on Port "+str(ports[1])
					if con_cmd:#if cmd socket connected,send cmd,let server product a new socket as data trasport socket
						con_s.send(CMD)
						con_s_tun,con_s_tun_addr = sock_s.accept()#data trasport socket,and start a new thread
						threading.Thread(target=self.forward_translate, args=(con_s_tun,con_c)).start()
		except Exception, e:
			print e
			sock_s.shutdown(socket.SHUT_RDWR)
			sock_s.close()
			sock_c.shutdown(socket.SHUT_RDWR)
			sock_c.close()
			#sys.exit()


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
			if args.remote: #start reverse socks5 mode
				while True:
					resocks5 = Socks5proxy()
					resocks5.reverse_socks5_main(args.remote,args.port)
			else: #start local socks5 mode
				while True:
					losocks5 = Socks5proxy()
					losocks5.local_socks5(args.port)
		elif args.forward: #start port farward mode
			while True:
				lforward = Socks5proxy()
				lforward.forward_main(args.forward)
	#except Exception,e:
	#	print e
	except KeyboardInterrupt:
		sys.exit(1)

if __name__ == '__main__':
	main()
