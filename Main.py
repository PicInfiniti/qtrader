from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys,sqlite3
import numpy as np

class Window(QGraphicsView):
	def __init__(self, DB='StockData.db', parent=None):
		super(Window, self).__init__(parent)
		# configure dataBase
		self.conn = sqlite3.connect(DB)
		self.cursor = self.conn.cursor()

		# extract all stock name stored in database ans store to List
		self.cursor.execute('SELECT Namad FROM StockInfo')
		self.List = np.array(self.cursor.fetchall())
		self.List = sorted(self.List.transpose()[0])
		
	# make all layout...	
		# tab widject
		self.tabs = QTabWidget() #creat tab object includes all tab
		self.tabs.setTabsClosable(True) #set tabs closable
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab) #you can connect it to a any fuction you made
		
		# Button  widject
		self.button = QPushButton('Add Plot')# make button
		self.button.clicked.connect(self.getItem)# connect to getitem function

		# linedit widget
		self.le = QLineEdit(self) #make linedit
		self.le.textChanged.connect(self.refine) #convert text to arbic
		self.completer = QCompleter() #make autocompleter
		self.completer.setModel(QStringListModel(self.List)) # add List of stock to completer
		self.le.setCompleter(self.completer) #connect copmpleter to linedit
		self.le.returnPressed.connect(self.pushButtonOK) #connect to pushButtonOK function after press ENTER

	def getItem(self):
		item, ok = QInputDialog.getItem(
			self, "select input dialog", "list of languages", self.List, 0, False)

	def refine(self):
		stockname = Persian(self.le.text())
		self.le.setText(stockname)

	def pushButtonOK(self):
		stockname = Persian(self.le.text())
		if stockname in self.List:
			self.plot(stockname)

def main():
	app = QApplication(sys.argv)
	ex = Window('StockData.db')
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
