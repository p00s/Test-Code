#!/usr/bin/env python
#coding:utf8

import socket,struct,argparse,sys,threading

BUF_SIZE=1024
FLAG = 0

class Socks5proxy(object):

	def socks5server(self,r,c):
		while True:
			if r.send(c.recv(BUF_SIZE)) <= 0:
				break 
			if c.send(r.recv(BUF_SIZE)) <= 0:
				break  
			
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
		print 7	
		c.send(reply)
		return r

	def lthread(self,c):
		try:
			print 22222
			c.recv(262)
			c.send(b"\x05\x00")
			print 2
			data = c.recv(BUF_SIZE)
			mode = ord(data[1])  
			addrtype = ord(data[3])
			print 3  
			if addrtype == 1:       # IPv4  
				addr = socket.inet_ntoa(data[4:8])
				port = (struct.unpack('!H', data[8:]))[0]  
			elif addrtype == 3:     # Domain name 
				length = struct.unpack('B', data[4:5])
				addr = data[5:5 + length]
				port = (struct.unpack('!H', data[5 + length:]))[0]
			print addr,port
			print 4
			r = self.remote(addr,port,mode,c)
			print 5
			if FLAG:
				self.socks5server(r,c)
		except Exception, e:
			raise e

	def lsocks5(self,port):#local socks5 server mode
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(("0.0.0.0", port))
			s.listen(5)
			print "[*]Socks5 server start on 0.0.0.0:",port
			while True:
				print 1
				c,address = s.accept()
				print "[*]Client from :",address[0],address[1]
				print 22222
				c.recv(262)
				c.send(b"\x05\x00")
				print 2
				data = c.recv(BUF_SIZE)
				mode = ord(data[1])  
				addrtype = ord(data[3])
				print 3  
				if addrtype == 1:       # IPv4  
					addr = socket.inet_ntoa(data[4:8])
					port = (struct.unpack('!H', data[8:]))[0]  
				elif addrtype == 3:     # Domain name 
					length = struct.unpack('B', data[4:5])
					addr = data[5:5 + length]
					port = (struct.unpack('!H', data[5 + length:]))[0]
				print addr,port
				print 4
				r = self.remote(addr,port,mode,c)
				print 5
				if FLAG:
					self.socks5server(r,c)
				#t = threading.Thread(target=self.lthread, args=(c,))
    			#t.start()
    			print 111
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
			#while True:
			s.recv(262)
			s.send(b"\x05\x00")
			data = s.recv(BUF_SIZE)
			mode = ord(data[1])  
			addrtype = ord(data[3])  
			if addrtype == 1:       # IPv4  
				addr = socket.inet_ntoa(data[4:8])
				port = (struct.unpack('!H', data[8:]))[0]  
			elif addrtype == 3:     # Domain name  
				length = struct.unpack('B', data[4:5])
				addr = data[5:5 + length]
				port = (struct.unpack('!H', data[5 + length:]))[0]
			
			r = self.remote(addr,port,mode,s)#forward requests
			if FLAG:
				self.socks5server(r,s)
		except Exception,e:
			print "[*]Remote listener port closed..."
			sys.exit(1)

	def forward(self,port_1,port_2):
		global BUF_SIZE

		try:
			s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 1
			s1.bind(("0.0.0.0", port_1))
			s1.listen(2)
			print "[*]Listen on 0.0.0.0:",port_1

			s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #port 2
			s2.bind(("0.0.0.0", port_2))
			s2.listen(2)
			print "[*]Listen on 0.0.0.0:",port_2
			while True:
				print 1
				c1,address1 = s1.accept()
				print "[*]Client from :"+address[0]+address[1]+" on Port "+port_1
				c2,address2 = s2.accept()
				print 2
				print "[*]Client from :"+address[0]+address[1]+" on Port "+port_2
				c1.send(c2.recv(BUF_SIZE)) #forward with two port
				c2.send(c1.recv(BUF_SIZE))

		except Exception, e:
			raise e

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
				lforward.forward(args.forward[0],args.forward[1])
	except Exception,e:
		print e
	#except KeyboardInterrupt:
		sys.exit(1)


if __name__ == '__main__':
	main()
