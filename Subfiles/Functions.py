from Subfiles.Classes import *

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
		
		western = QAction(QIcon("Subfiles/pic/wcs.png"), "WesternCandlestick", self)
		tb.addAction(western)
		payani = QAction(QIcon("Subfiles/pic/P.png"), "Payani", self)
		tb.addAction(payani)
		boundry = QAction(QIcon("Subfiles/pic/B.png"), "Boundary", self)
		tb.addAction(boundry)
		
		tb.actionTriggered[QAction].connect(self.toolbtnpressed)
		
def assign(self,b):
	self.CurrentNamad = b
