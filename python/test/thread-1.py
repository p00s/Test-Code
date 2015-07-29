#coding:utf8

import threading
import time



deep = 2
thread = 2
flag = 0
mylock = threading.RLock()
def tree(links):
	global flag
	global deep
	while flag <= deep:
		flag = flag+1
		print "links " ,links
		print "flag" ,flag
		for r in links:
			def work(r):
				#mylock.acquire()
				tree_links = [x for x in range(r+5)]	
				print "tree_links",tree_links
				time.sleep(0.5)
				#mylock.release()

			while  threading.active_count() < thread:
				sp=threading.Thread(target=work,args=(r,))
				sp.start()
				#sp.join()
				print "start : "




if __name__ == '__main__':
	l = [2,3,4,5,6,7,8]
	tree(l)