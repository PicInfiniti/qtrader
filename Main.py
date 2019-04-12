from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Window(QGraphicsView):
	def __init__(self, DB='StockData.db', parent=None):
		super(Window, self).__init__(parent)
		# configure dataBase
		self.conn = sqlite3.connect(DB)
		self.cursor = self.conn.cursor()
		

def main():
	app = QApplication(sys.argv)
	ex = Window('StockData.db')
	ex.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
