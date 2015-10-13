#!/usr/bin/env python
#coding:utf8


from Tkinter import *
from FileDialog import *
import tkMessageBox
#author:yzqycn
#http://www.yzqy.cc

class App(object):
	"""docstring for App"""
	def __init__(self, arg):
		super(App, self).__init__()
		self.root = arg
		self.root.title("Notepad")
		self.root.geometry("800x600+450+200")
		self.status=0
	def do(self):
		pass
	def about(self):
		about = Toplevel()
		about.title("Notepad about")
		about.geometry("200x150+650+250")
		Message(about,text="Notepad\nby:yzqycn\nhttp://www.yzqy.cc",justify=CENTER,width=150).pack()
		about.mainloop()

	def callmessagebox(self,event=None):
		#open a new windows alert messagebox
		ans =tkMessageBox.askyesno("Warning",'Not save this File?')
		if ans:
			self.t1.delete(0.0,END)

	def callquit(self):
		#quit program ask if save file
		ans =tkMessageBox.askyesno("Warning",'Not save this File and quit?')
		if ans:
			self.root.quit()

	def motion(self,event):
		#get mourse position
		self.x, self.y = event.x, event.y

	def statubar(self):
		#status bar,but not sussess!
		if self.status == 0:
			#x=self.root.winfo_pointerx()
			#y=self.root.winfo_pointery()
			self.statext = "Current: row = "+str(self.x)+"			column = "+str(self.y)
			self.statusbar = Message(self.root,text=self.statext,anchor=W)
			self.statusbar.pack(side =BOTTOM,fill=X)
			self.statusbar.config(text=self.statext)
			self.statusbar.update_idletasks()
			self.status=1
		else:
			self.statusbar.config()
			self.status=0

	def openfile(self,event=None):
		#open file FileDialog
		fd = LoadFileDialog(self.root)
		filename = fd.go()
		try:
			fp = open(filename, 'r').read()
			self.t1.delete(0.0,END)
			self.t1.insert(END,fp)
		except:
			tkMessageBox.showwarning("warning",'Could not open File:%s'%filename)

	def save(self,event=None):
		#save File FileDIalog
		fd = SaveFileDialog(self.root) 
		filename= fd.go() 
		newfile = open(filename, 'w') 
		content = self.t1.get(0.0, END) 
		newfile.write(content) 
		newfile.close() 

	def copy(self, event=None):
		#copy method
		self.t1.clipboard_clear()
		text = self.t1.get("sel.first", "sel.last")
		self.t1.clipboard_append(text)
	
	def cut(self, event=None):
		#cut method
		self.copy()
		self.t1.delete("sel.first", "sel.last")

	def paste(self, event=None):
		#paste method
		text = self.t1.selection_get(selection='CLIPBOARD')
		self.t1.insert('insert', text)

	def selectText(self,event=None):
		#select all text method,but "ctrl + a" not sussess!
		self.t1.tag_add("sel","0.0","end")

	def popmr(self,event):
		#press mouse right pop menu
		self.mrmenu.post(event.x_root,event.y_root)
		self.onright =1
	def pushmr(self,event):
		#If right menu poped,press mouse left close
		if self.onright == 1:
			self.mrmenu.unpost()
			self.onright =0
	def deletes(self):
		#delete select text
		self.t1.delete("sel.first", "sel.last")

	def run(self):
		#Main 
		self.t1=Text(self.root,bd=2)
		self.t1.pack(side="left", fill="both", expand=True)
		#create Text
		myscrollbar=Scrollbar(self.root,orient="vertical",command=self.t1.yview)
		self.t1.configure(yscrollcommand=myscrollbar.set)
		myscrollbar.pack(side="right",fill="y")
		#create scrollbar on right text

		self.menubar = Menu(self.root)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="New(Ctrl+n)", command=self.callmessagebox)
		self.filemenu.add_command(label="Open(Ctrl+o)", command=self.openfile)
		self.filemenu.add_command(label="Save(Ctrl+s)", command=self.save)
		self.filemenu.add_command(label="Exit", command=self.callquit)
		self.menubar.add_cascade(label="File", menu=self.filemenu)
		#FIle menu

		self.editmenu = Menu(self.menubar, tearoff=0)
		self.editmenu.add_command(label="Cut(ctrl+x)", command=self.cut)
		self.editmenu.add_command(label="Copy(ctrl+c)", command=self.copy)
		self.editmenu.add_command(label="Paste(ctrl+v)", command=self.paste)
		self.editmenu.add_command(label="Delete", command=self.deletes)
		self.editmenu.add_command(label="Select All(ctrl+a)", command=self.selectText)
		self.editmenu.add_command(label="Find", command=self.root.quit)
		self.menubar.add_cascade(label="Edit", menu=self.editmenu)
		#edit menu

		self.viewmenu = Menu(self.menubar,tearoff = 0)
		self.viewmenu.add_command(label="Status bar",command= self.do)
		self.menubar.add_cascade(label = "view",menu = self.viewmenu)
		#view menu

		self.helpmenu = Menu(self.menubar, tearoff=0)
		self.helpmenu.add_command(label="Help Index", command=self.do)
		self.helpmenu.add_command(label="About...", command=self.about)
		self.menubar.add_cascade(label="Help", menu=self.helpmenu)
		self.root.config(menu = self.menubar)
		#help menu

		self.mrmenu = Menu(self.t1, tearoff=0)
		self.mrmenu.add_command(label="Cut", command=self.cut)
		self.mrmenu.add_command(label="Copy", command=self.copy)
		self.mrmenu.add_command(label="Paste", command=self.paste)
		self.mrmenu.add_command(label="Delete", command=self.deletes)
		self.mrmenu.add_command(label="Select all", command=self.selectText)
		self.onright = 0
		#moouse right menu

		self.t1.bind('<Control-c>', self.copy)
		self.t1.bind('<Control-x>', self.cut)
		self.t1.bind('<Control-v>', self.paste)
		self.t1.bind("<Button-3>",self.popmr)
		self.t1.bind("<Button-1>",self.pushmr)
		self.t1.bind('<Control-c>',self.selectText)
		self.root.bind('<Motion>', self.motion)
		self.t1.bind('<Control-n>', self.callmessagebox)
		self.t1.bind('<Control-o>', self.openfile)
		self.t1.bind('<Control-s>', self.save)
		#listing key and call method

if __name__ == '__main__':
	main = Tk()
	app = App(main)
	app.run()
	main.mainloop()

		
