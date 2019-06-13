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
from Subfiles.Indicators import *

class Plot_Panel(QWidget):
	'''S این کلاس شامل تمام اشیای داخل تب می‌باشد'''
	def __init__(self, StockName, data ,parent=None):
		super(Plot_Panel, self).__init__(parent) #I don't what is this; but don't work without it
		self.Property = {'StockName': StockName,
		        'Bars': 300,
		        'WesternCandlestick':1,
		        'Payani': 1,
		        'Boundary': 1,
		        'Cross': 0,
		        'Period':0,
		        'PeriodP':False
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
		self.proxy = pg.SignalProxy(self.Pax.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
		self.vLine = pg.InfiniteLine(angle=90, movable=False)
		self.hLine = pg.InfiniteLine(angle=0, movable=False, label='Price={value:0.2f} irr', labelOpts={'position':.1, 'color': (200,200,100), 'fill': (200,200,200,50)})

		if self.Property['Cross']:
			self.Pax.addItem(self.vLine, ignoreBounds=True)
			self.Pax.addItem(self.hLine, ignoreBounds=True)
		# add graphical object to Pax
		if self.Property['WesternCandlestick']:
			self.Pax.addItem(WesternCandlestick(
				self.data[-self.Property['Bars']:,[0,1,2,3,4,5]])) #add WesternCandlestick
		if self.Property['Payani']:
			self.Pax.addItem(Payani(
				self.data[-self.Property['Bars']:,[0,3]])) #add Payani
		if self.Property['Boundary']:
			self.Pax.addItem(Boundary(
				self.data[-self.Property['Bars']:,[0,3]])) #add Boundary
		if self.Property['Period']:
			self.Pax.addItem(Period2(
				self.data[-self.Property['Bars']:,[0,1,2]], self.Property['PeriodP'][0], self.Property['PeriodP'][1]))

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
		if self.Property['Cross']:
			self.Pax.addItem(self.vLine, ignoreBounds=True)
			self.Pax.addItem(self.hLine, ignoreBounds=True)
		if self.Property['WesternCandlestick']:
			self.Pax.addItem(WesternCandlestick(
				self.data[-self.sl.value():,[0,1,2,3,4,5]])) #plot new WesternCandlestick
		if self.Property['Payani']:
			self.Pax.addItem(Payani(
				self.data[-self.sl.value():,[0,3]])) #add Payani
		if self.Property['Boundary']:
			self.Pax.addItem(Boundary(
				self.data[-self.sl.value():,[0,3]])) #add Boundary
		if self.Property['Period']:
			self.Pax.addItem(Period2
				(self.data[-self.sl.value():,[0,1,2]], self.Property['PeriodP'][0], self.Property['PeriodP'][1]))
		    
	def mouseMoved(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.Pax.sceneBoundingRect().contains(pos):
			mousePoint = self.Pax.vb.mapSceneToView(pos)
			self.vLine.setPos(mousePoint.x())
			self.hLine.setPos(mousePoint.y())

class InputDialog(QWidget):
	def __init__(self):
		text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
		self.Return(text,ok)
	
	def Return(self,text,ok):
		if ok:
			print(56)
		else:
			self.Property['Period'] = 0
			self.CurrentNamad.widget().valueChanged()

