from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel)
import sys

class Example(QWidget):

	def __init__(self):
		super().__init__()
		self.showDialog()

	def showDialog(self):

		text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
		if text and ok:
			print(str(text))
		if not 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
