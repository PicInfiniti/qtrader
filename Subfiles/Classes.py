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
from Subfiles.Functions import * 
from Subfiles.DataBase import *

class Plot_Panel(QWidget):
	'''S این کلاس شامل تمام اشیای داخل تب می‌باشد'''
	def __init__(self, StockName, data ,DB='StockData.db', parent=None):
		super(Plot_Panel, self).__init__(parent) #I don't what is this; but don't work without it
				# configure dataBase
		self.conn = sqlite3.connect(DB)
		self.cursor = self.conn.cursor()
		
		self.Property = {'StockName': StockName,
		        'Bars': 300,
		        'WesternCandlestick':0,
		        'Payani': 1,
		        'Boundary': 0,
		        'Cross': 0,
		        'Period':0,
		        'PeriodP':False,
		        'COV':0,
		        'COVP': False
		        } #store property of current tab

		self.data = data #stock history (open, close, ...)
		self.dicdata = DicData(data)
		Number_of_Bars = len(self.data) #len of history

		# Ledft Slider with lable
		self.sl = QSlider() #make slider
		self.label = QLabel() #make lable for slider
		self.label.setText(str([Number_of_Bars, self.Property['Bars']]
		                 [Number_of_Bars > self.Property['Bars']])) #set defult lable
		self.sl.setMinimum(25) #set minimu slider value
		self.sl.setMaximum(Number_of_Bars) #set maxinmum slider value
		self.sl.setValue([Number_of_Bars, self.Property['Bars']]
		                 [Number_of_Bars > self.Property['Bars']]) #set defult slider value
		self.sl.valueChanged.connect(self.valueChanged) #connet to self.valueChanged function when someone change slider
		
		# right Slider with lable
		self.rsl = QSlider() #make slider
		self.rlabel = QLabel() #make lable for slider
		self.rlabel.setText(str(0)) #set defult lable
		self.rsl.setMaximum(self.sl.value()-25) #set maxinmum slider value
		self.rsl.setValue(0) #set defult slider value
		self.rsl.valueChanged.connect(self.valueChanged) #connet to self.valueChanged function when someone change slider
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
				
		if self.Property['COV']:
			data = self.Property['COVP']
			self.Pax.addItem(Payani(
				data[-self.Property['Bars']:,[0,3]],color='r')) #add COV

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
		
		# make a vertical layout right slider
		Vlayout = QVBoxLayout() 
		Vlayout.addWidget(self.rlabel) #add lable to Vlayout
		Vlayout.addWidget(self.rsl) #add slider to Vlayout
		Hlayout.addLayout(Vlayout)
		# add every thing to Mlayout
		self.setLayout(Hlayout)

	def valueChanged(self): #run when slider changed
		self.sl.setMinimum(self.rsl.value()+25)
		self.rsl.setMaximum(self.sl.value()-25)
		self.label.setText(str(self.sl.value())) #update slider lable
		self.rlabel.setText(str(self.rsl.value())) #update slider lable
		self.Pax.clear() #clearPax axes for new plot
		if self.Property['Cross']:
			self.Pax.addItem(self.vLine, ignoreBounds=True)
			self.Pax.addItem(self.hLine, ignoreBounds=True)
		if self.Property['WesternCandlestick']:
			self.Pax.addItem(WesternCandlestick(
				self.data[-self.sl.value():len(self.data)-self.rsl.value(),[0,1,2,3,4,5]])) #plot new WesternCandlestick
		if self.Property['Payani']:
			self.Pax.addItem(Payani(
				self.data[-self.sl.value():len(self.data)-self.rsl.value(),[0,3]])) #add Payani
		if self.Property['Boundary']:
			self.Pax.addItem(Boundary(
				self.data[-self.sl.value():len(self.data)-self.rsl.value(),[0,3]])) #add Boundary
		if self.Property['Period']:
			self.Pax.addItem(Period2
				(self.data[-self.sl.value():,[0,1,2]], self.Property['PeriodP'][0], self.Property['PeriodP'][1]))
		if self.Property['COV']:
			data = self.Property['COVP']
			self.Pax.addItem(Payani(
				data[-self.sl.value():len(data)-self.rsl.value(),[0,3]],color='r')) #add COV    
				
	def mouseMoved(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.Pax.sceneBoundingRect().contains(pos):
			mousePoint = self.Pax.vb.mapSceneToView(pos)
			self.vLine.setPos(mousePoint.x())
			self.hLine.setPos(mousePoint.y())
			if int(mousePoint.x()) in self.dicdata.keys():
				data = ModifyDictaToPrint(self.dicdata[int(mousePoint.x())])
				self.parentWidget().parentWidget().statusBar.showMessage(
					mdates.num2date(int(mousePoint.x())).strftime('%Y.%m.%d')+", "+data)
					
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

class DateDialog(QDialog):
    def __init__(self, parent = None):
        super(DateDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.datetime = QDateTimeEdit(self)
        self.datetime.setCalendarPopup(True)
        self.datetime.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog
    def dateTime(self):
        return self.datetime.dateTime()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDateTime(parent = None):
        dialog = DateDialog(parent)
        result = dialog.exec_()
        date = dialog.dateTime()
        return (date.date(), date.time(), result == QDialog.Accepted)
