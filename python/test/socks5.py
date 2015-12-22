import socket,struct,time

BUF_SIZE=1024
FLAG = 0

class Rsocks5searver(object):
	"""docstring for ClassName"""
	def __init__(self, dport,daddr):
		super(ClassName, self).__init__()
		self.dport = dport
		self.daddr = socket.gethostbyname(daddr)
	def socks5server(self,s):
		while 1:
			s.recv(4096)
			
	def remote(self,ipaddr,port,mode):
		global FLAG
		try:
			r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			r.connect((ipaddr, port))
			if mode==1:#tcp type
				reply = b"\x05\x00\x00\x01"
				FLAG = 1
			else:#udp not suport
				reply = b"\x05\x07\x00\x01" #
				FLAG = 0

			local = r.getsockname()
			reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
		except Exception, e:
			reply = b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
			FLAG = 0
		r.send(reply)
		return r


	def socks5(self):
		global BUF_SIZE
		global FLAG

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.daddr, self.dport))
			print "[*]Tcp connected to", self.daddr, self.dport
			s.recv(262)
			s.send(b"\x05\x00")
			data = s.recv(BUF_SIZE)
			mode = ord(data[1])  
			addrtype = ord(data[3])  
			if addrtype == 1:       # IPv4  
				addr = socket.inet_ntoa(data[4:8])
				port = struct.unpack('!H', data[8:])  
			elif addrtype == 3:     # Domain name  
		                length = struct.unpack('B', data[4:5])
		                addr = data[5:5 + length]
		                port = struct.unpack('!H', data[5 + length:])

		    r = remote(addr,port,mode)
		    if FLAG:
		    	socks5server()

            

          	s.send(reply)
          	self.socksserver(s)
        except socket.error:  
            print 'socket error'
				
		except Exception, e:
			raise e


