import requests,ast,csv,codecs, sys, random, os
from math import ceil
import numpy as np
import datetime as dt
import pyqtgraph as pg
from matplotlib.ticker import Formatter
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Subfiles.Subclasses import *

class Plot_Panel(QWidget):
	'''S این کلاس شامل تمام اشیای داخل تب می‌باشد'''
	def __init__(self, StockName, data ,parent=None):
		super(Plot_Panel, self).__init__(parent) #I don't what is this; but don't work without it
		self.Property = {'StockName': StockName,
				'Bars': 300,
				'Current_Indicator': 'Shenavar'
				} #store property of current tab

		self.data = data #stock history (open, close, ...)
		Number_of_Bars = len(self.data) #len of history

		# Slider with lable
		self.sl = QSlider() #make slider
		self.label = QLabel() #make lable for slider
		self.label.setText(str([Number_of_Bars, self.Property['Bars']]
		                 [Number_of_Bars > self.Property['Bars']])) #set defult lable
		self.sl.setMinimum(25) #set minimu slider value
		self.sl.setMaximum(Number_of_Bars) #set maxinmum slider value
		self.sl.setValue([Number_of_Bars, self.Property['Bars']]
		                 [Number_of_Bars > self.Property['Bars']]) #set defult slider value

		self.sl.valueChanged.connect(self.valueChanged) #connet to self.valueChanged function when someone change slider
		# create price axis
		self.Pfigure = pg.GraphicsWindow()
		self.Pax = self.Pfigure.addPlot(0, 0, axisItems={'bottom': TimeAxisItem(orientation='bottom')}) #make axis with & custom timeaxis
		self.Pax.showGrid(x=True, y=True)

		# add graphical object to Pax
		self.Pax.addItem(WesternCandlestick(
			self.data[-self.Property['Bars']:,[0,1,2,3,4,5]])) #add WesternCandlestick

		# Hlayout is main layout
		Mlayout = QVBoxLayout()

		# make a vertical layout
		Vlayout = QVBoxLayout() 
		Vlayout.addWidget(self.label) #add lable to Vlayout
		Vlayout.addWidget(self.sl) #add slider to Vlayout

		# make a horizontal layout
		Hlayout = QHBoxLayout() 
		Hlayout.addLayout(Vlayout)
		Hlayout.addWidget(self.Pfigure) #add figure to Hlyaout

		# add every thing to Mlayout
		self.setLayout(Hlayout)

	def valueChanged(self): #run when slider changed
		self.label.setText(str(self.sl.value())) #update slider lable
		self.Pax.clear() #clearPax axes for new plot
		self.Pax.addItem(WesternCandlestick(
			self.data[-self.sl.value():,[0,1,2,3,4,5]])) #plot new WesternCandlestick

class WesternCandlestick(QGraphicsObject): #make WesternCandlestick QGraphicsObject for plot price history
	# order data: time, open, close, min, max
	def __init__(self, data):
		QGraphicsObject.__init__(self)
		self.data = data  #data must have fields: time, Hight, Low, Payani, close, Open
		self.generatePicture() #generate picture

	def generatePicture(self):
		## pre-computing a QPicture object allows paint() to run much more quickly, 
		## rather than re-drawing the shapes every time.
				
		OFFSET = .4
		self.picture = QPicture()
		p = QPainter(self.picture)
		p.setPen(pg.mkPen('c',width=2))

		Date, Hight, Low, Payani, Close, Open = self.data[0]
		p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
		p.drawLine(QPointF(Date, Payani), QPointF(Date+OFFSET, Payani))
		p.drawLine(QPointF(Date, Close), QPointF(Date+OFFSET, Close))
		p.drawLine(QPointF(Date-OFFSET, Open), QPointF(Date, Open))
		PreviousBar = Payani

		for (Date, Hight, Low, Payani, Close, Open) in self.data[1:]:
			p.setPen(pg.mkPen('y',width=2))
			p.drawLine(QPointF(Date, Payani), QPointF(Date+OFFSET, Payani))
			p.setPen(pg.mkPen('y',width=.5,style=Qt.DotLine))
			p.drawLine(QPointF(Date-OFFSET, int(1.05*PreviousBar)), QPointF(Date+OFFSET, int(1.05*PreviousBar)))
			p.drawLine(QPointF(Date-OFFSET, ceil(.95*PreviousBar)), QPointF(Date+OFFSET, ceil(.95*PreviousBar)))
			p.drawLine(QPointF(Date, ceil(.95*PreviousBar)), QPointF(Date, int(1.05*PreviousBar)))

			p.setPen(pg.mkPen(['r','g'][PreviousBar < Close],width=2))
			p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
			p.drawLine(QPointF(Date, Close), QPointF(Date+OFFSET, Close))
			p.drawLine(QPointF(Date-OFFSET, Open), QPointF(Date, Open))
			
			PreviousBar = Payani
		p.end()

	def paint(self, p, *args):
		p.drawPicture(0, 0, self.picture)

	def boundingRect(self):
		## boundingRect _must_ indicate the entire area that will be drawn on
		## or else we will get artifacts and possibly crashing.
		## (in this case, QPicture does all the work of computing the bouning rect for us)

		return QRectF(self.picture.boundingRect())

#menuBar
def MenuBar(self):
	mainMenu = self.menuBar()
	fileMenu = mainMenu.addMenu('File')
	IndMenu = mainMenu.addMenu('Indicators')
	viewMenu = mainMenu.addMenu('View')
	searchMenu = mainMenu.addMenu('Search')
	toolsMenu = mainMenu.addMenu('Tools')
	helpMenu = mainMenu.addMenu('Help')
#File
	exitButton = QAction('Exit', self)
	exitButton.setShortcut('Ctrl+Q')
	exitButton.setStatusTip('Exit application')
	exitButton.triggered.connect(self.close)
	fileMenu.addAction(exitButton)

#Indicators
	Custom = IndMenu.addMenu("Custom")
	
#Tool Bar
def ToolBar(self):
		tb = self.addToolBar("Indicators")
		
		new = QAction("new",self)
		tb.addAction(new)

		open = QAction("open",self)
		tb.addAction(open)
		save = QAction("save",self)
		tb.addAction(save)
		tb.actionTriggered[QAction].connect(self.toolbtnpressed)
