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
