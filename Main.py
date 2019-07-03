from Subfiles.DataBase import *
from Subfiles.Classes import *
from Subfiles.Functions import * 


class MainWindow(QMainWindow):
	def __init__(self, DB='StockData.db', parent = None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("QTrader")
		self.CurrentNamad = 0
		# configure dataBase
		self.conn = sqlite3.connect(DB)
		self.cursor = self.conn.cursor()

		# extract all stock name stored in database ans store to List
		self.cursor.execute('SELECT Namad FROM StockInfo')
		self.List = np.array(self.cursor.fetchall())
		self.List = sorted(self.List.transpose()[0])

		# linedit widget
		bANDle = QWidget()
		self.le = QLineEdit(self) #make linedit
		self.le.textChanged.connect(self.refine) #convert text to arbic
		self.completer = QCompleter() #make autocompleter
		self.completer.setModel(QStringListModel(self.List)) #add List of stock to completer
		self.le.setCompleter(self.completer) #connect copmpleter to linedit
		self.le.returnPressed.connect(self.pushButtonOK) #connect to pushButtonOK function after press ENTER
		self.b = QPushButton("COV")
		self.b.setCheckable(True)
		Hlayout = QHBoxLayout()
		Hlayout.addWidget(self.b)
		Hlayout.addWidget(self.le)
		bANDle.setLayout(Hlayout)
		
		self.setCentralWidget(bANDle)
		for stockname in ['وتجارت']:
			self.plot(Persian(stockname))
		
		#Menu Bar
		MenuBar(self)
		#Tool Bar
		ToolBar(self)
		#statusBar
		self.statusBar = QStatusBar()
		self.setStatusBar(self.statusBar)
		self.statusBar.showMessage("Great SiaVash")

	def toolbtnpressed(self,a):
		if a.text()=='Period':
			text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
			if '-' in text and ok:
				jump, walker = text.split('-')
				walker = mdates.date2num(jdt.date.togregorian(dt.datetime.strptime(walker, '%Y%m%d')))#BBBBUUUUGGGG
				self.CurrentNamad.widget().Property['PeriodP'] = [int(jump), walker]
				self.CurrentNamad.widget().Property['Period'] = 1
				self.CurrentNamad.widget().Plot()
				return
				
			elif not text and ok:
				self.CurrentNamad.widget().Property['PeriodP']=False
				self.CurrentNamad.widget().Property['Period'] = 0
				self.CurrentNamad.widget().Plot()
				return
			else:
				return
	
				
		self.CurrentNamad.widget().Property[a.text()] = [0,1][self.CurrentNamad.widget().Property[a.text()] == 0]
		self.CurrentNamad.widget().Plot()
		
	def refine(self): #refine entry text in self.le
		stockname = Persian(self.le.text())
		self.le.setText(stockname)		

	def pushButtonOK(self): #call self.plot function
		stockname = Persian(self.le.text())
		if stockname in self.List:
			self.plot(stockname)

	def plot(self, stockname, Bars=300): #open new tab and plot on it
		if self.b.isChecked():
			Namad = self.CurrentNamad.widget()
			Pax = Namad.Pax
			data = self.get_data(stockname)
			Pax.addItem(Payani(
				data[:,[0,3]],color='r')) #add COV   
			
		else:
			dock = QDockWidget(stockname,self)
			dock.mousePressEvent = lambda x: assign(self, dock)

			dock.setWidget(Plot_Panel(stockname, self.get_data(stockname)))
			self.addDockWidget(Qt.TopDockWidgetArea, dock)
			self.CurrentNamad = dock
			
		
	def get_data(self, stockname): #extarct history from database
		try:
			if not self.cursor.execute(
					'SELECT * FROM sqlite_master WHERE name = "NAMAD"'.replace('NAMAD', stockname)).fetchone():
				Get_Csv(id2stock(stockname))# if history not exit in data base download it
			
			elif self.cursor.execute(
	 				'SELECT * FROM "NAMAD" LIMIT 1'.replace('NAMAD', stockname)).fetchone()[0]!=int(dt.date.today().strftime('%Y%m%d')):
				Get_Csv(id2stock(stockname)) #if data exist but not uptodate update it
		except:
			print ("Please Check your CONNECTION")
				
		self.cursor.execute(
				'SELECT * FROM "NAMAD" ORDER BY Date ASC'.replace('NAMAD', stockname)) #get and sort data ascendig; 0 index has oldest date. [20161017, 20161018, ..., 20190413]
		data = np.array(self.cursor.fetchall(), int) #store data in numpy array with int format
		for i in range(len(data)): #turn date to matplotlib datatime format
			data[i][0] = mdates.date2num(
				dt.datetime.strptime(str(data[i][0]), '%Y%m%d'))
				
		return data

def main():
	app = QApplication(sys.argv)
	ex = MainWindow()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
