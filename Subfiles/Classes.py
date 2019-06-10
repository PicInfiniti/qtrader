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
		# add graphical object to Pax
		self.Pax.addItem(Payani(
			self.data[-self.Property['Bars']:,[0,3]])) #add Payani
		
		self.Pax.addItem(Payani(
			self.data[-self.Property['Bars']:,[0,3]])) #add Boundary
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
		self.Pax.addItem(Payani(
			self.data[-self.sl.value():,[0,3]])) #add Payani
			
		self.Pax.addItem(Boundary(
			self.data[-self.sl.value():,[0,3]])) #add Boundary


