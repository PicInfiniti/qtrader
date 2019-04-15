import requests,ast,csv,codecs, sys, random, os
import numpy as np
import pyqtgraph as pg
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import Formatter
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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

		# create price axis
		self.Pfigure = pg.GraphicsWindow()
		self.Pax = self.Pfigure.addPlot(0, 0)
		self.Pax.showGrid(x=True, y=True)

		# Mlayout is main layout
		self.Mlayout = QVBoxLayout()
		self.Mlayout.addWidget(self.Pfigure)

		# add every thing to Mlayout
		self.setLayout(self.Mlayout)

class WesternCandlestick(QGraphicsObject): #make WesternCandlestick QGraphicsObject for plot price history
	# order data: time, open, close, min, max
	def __init__(self, data):
		QGraphicsObject.__init__(self)
		self.data = data  ## data must have fields: time, Payani ,Hight, Low, close

		self.generatePicture()

	def generatePicture(self):
		## pre-computing a QPicture object allows paint() to run much more quickly, 
		## rather than re-drawing the shapes every time.
				
		OFFSET = .4
		self.picture = QPicture()
		p = QPainter(self.picture)
		p.setPen(pg.mkPen('c',width=2))

		Date, Payani, Hight, Low, Close = self.data[0]
		p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
		p.drawLine(QPointF(Date, Payani), QPointF(Date+OFFSET, Payani))
		p.drawLine(QPointF(Date-OFFSET, Close), QPointF(Date, Close))
		PreviousBar = Payani

		for (Date, Payani, Hight, Low, Close) in self.data[1:]:
			p.setPen(pg.mkPen(['r','g'][PreviousBar < Close],width=2))
			p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
			p.drawLine(QPointF(Date, Payani), QPointF(Date+OFFSET, Payani))
			p.drawLine(QPointF(Date-OFFSET, Close), QPointF(Date, Close))
			PreviousBar = Payani
		p.end()

	def paint(self, p, *args):
		p.drawPicture(0, 0, self.picture)

	def boundingRect(self):
		## boundingRect _must_ indicate the entire area that will be drawn on
		## or else we will get artifacts and possibly crashing.
		## (in this case, QPicture does all the work of computing the bouning rect for us)

		return QRectF(self.picture.boundingRect())

