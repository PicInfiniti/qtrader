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
		
	# make all layout-------	
		# Initialize tab layout
		self.tabs = QTabWidget() #creat tab object includes all tab
		self.tabs.setTabsClosable(True) #set tabs closable
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab) #you can connect it to a any fuction you made
		

def main():
	app = QApplication(sys.argv)
	ex = Window('StockData.db')
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
