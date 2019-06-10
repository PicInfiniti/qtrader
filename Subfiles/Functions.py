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
		
		new = QAction("new",self)
		tb.addAction(new)

		open = QAction("open",self)
		tb.addAction(open)
		save = QAction("save",self)
		tb.addAction(save)
		tb.actionTriggered[QAction].connect(self.toolbtnpressed)
		
def assign(self,b):
	self.CurrentNamad = b
