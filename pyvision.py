#!/usr/bin/python
#References
##http://www.tkdocs.com/tutorial/firstexample.html
##http://www.tutorialspoint.com/python/python_gui_programming.htm
##http://stackoverflow.com/questions/32379042/how-can-i-save-the-output-of-a-python-function-that-i-run-using-a-tkinter-button
##http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed

import Tkinter
from Tkinter import *
import tkMessageBox
import scipy.io as sio

from numpy import *

import matplotlib
from matplotlib import cm
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class Pyvision(object):

    def __init__(self):
	"""
	Creates an instance of Pyvision
	"""

	#Parameters
	self.positions = sio.loadmat('arrayPositions512.mat')['positions']
	self.xmax = max(self.positions[:,0])
	self.ymax = max(self.positions[:,1])
	self.plotBuff = 50
	self.eithr = -3
	#self.eibound = -30
	self.colmap = cm.gist_stern


	#Root Window
	top = Tk()
	top.title('PyVision')

	#Frames
	inputframe = Frame(top)
	inputframe.pack(side = LEFT)

	plotframe = Frame(top)
	plotframe.pack(side = RIGHT)

	#Constituents of inputframe
	##Frame that contains entry box
	entryframe = Frame(inputframe)
	entryframe.pack(side = TOP)

	##Constituents of entryframe
	topeframe = Frame(entryframe)
	topeframe.pack(side = TOP)

	boteframe = Frame(entryframe)
	boteframe.pack(side = BOTTOM)

	##Frame that contains the lists
	listframe = Frame(inputframe)
	listframe.pack(side = BOTTOM, fill = Y, expand = 1)

	##Input box label text
	inputlab = Label(boteframe, text = 'Eimat Location:')
	inputlab.pack(side = LEFT)

	##Eimat location entry box
	self.inputent = Entry(boteframe, bd = 5)
	self.inputent.pack(side = LEFT)
	self.inputent.delete(0, END)
	self.inputent.insert(0, 'C:\Users\Aruna\Documents\Medical_School\CC_Research\my_code\pyvision\eimat_2016-04-21-6.mat')

	##Indicator as to whether loaded
	self.indLab = Label(topeframe, text = 'Not loaded', anchor = N, font = ('Helvetica',16), bg = 'red', pady = 7)
	self.indLab.pack()

	##Loads eimat
	inputbut = Button(boteframe, text = 'Go!', command = self.inputbutCallBack)
	inputbut.pack(side = RIGHT)

	#Constituents of listframe
	##Scroll bar for cell ID list
	iscroll = Scrollbar(listframe)
	iscroll.pack(side = LEFT, fill = Y)

	##Selectable cell ID list
	self.inputlist = Listbox(listframe, yscrollcommand = iscroll.set, height = 30)
	self.inputlist.bind('<<ListboxSelect>>', self.onselect)
	self.inputlist.pack(side = TOP, fill = Y, expand = 1)
	iscroll.config(command = self.inputlist.yview)

	#Constituents of plotframe
	##Pyplot default
	self.mainPlot = Figure(dpi = 100)
	self.a = self.mainPlot.add_subplot(111)
	self.a.text(3, 8, 'boxed italics text in data coords', style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

	##Canvas to host Figure
	self.canvas = FigureCanvasTkAgg(self.mainPlot, master=top)
	self.canvas.show()
	self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	##Add toolbar (optional)
	toolbar = NavigationToolbar2TkAgg(self.canvas, top)
	toolbar.update()
	self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

	##Add text annotate button
	elecBut = Button(listframe, text = 'Show Electrode #s', command = self.elecButCallBack)
	elecBut.pack(side = BOTTOM)

	#Run GUI
	top.mainloop()

    def inputbutCallBack(self):
	"""
	Loads eimat provided valid filepath
	"""
	ie = self.inputent.get()
	if not ie:
	    tkMessageBox.showerror('Error','No Eimat location given')
	    return
	else:
	    try:
		eidict = sio.loadmat(ie)
		self.clist = eidict['x'][0]
		self.eimin = amin(eidict['allEIs'], axis = 2)
		self.eimin[self.eimin > self.eithr] = 0
		self.indLab.configure(bg = 'green', text = 'Loaded')
		cvec = [str(i) for i in ones((len(self.positions)))]
		self.showlist(cvec)
		return self
	    except IOError:
		tkMessageBox.showerror('Error','File not found')

    def showlist(self, cvec):
	"""
	Provided eimat has been loaded, shows cell IDs
	"""
	for c in self.clist: self.inputlist.insert(END, str(c))
	self.showflg = 1
	self.drawFig(cvec)
	return self
    
    def drawFig(self, cvec):
	"""
	Given a cell, draws a scatter plot showing its EI
	"""
	self.a.clear()
	self.a.scatter(self.positions[:,0], self.positions[:,1], s=120, c = cvec, edgecolors='b', cmap = self.colmap)
	self.a.set_ylim([-self.ymax - self.plotBuff, self.ymax + self.plotBuff])
	self.a.set_xlim([-self.xmax - self.plotBuff, self.xmax + self.plotBuff])
	self.canvas.show()

    def onselect(self, evt):
	sel = self.inputlist.curselection()[0]
	c = self.getC(sel)

    def getC(self, cidx):
	ei = self.eimin[cidx]
	self.drawFig(ei)

    def elecButCallBack(self):
	for i,p in enumerate(self.positions):
	    self.a.annotate(str(i+1),(p[0]-20,p[1]+20),fontsize=6,fontweight='bold')
	self.canvas.show()



Pyvision()
