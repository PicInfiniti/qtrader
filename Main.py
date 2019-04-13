from Subfiles.DataBase import *
from Subfiles.Classes import *
from datetime import date

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
		
	# make all widget...	
		# tab widject
		self.tabs = QTabWidget() #creat tab object includes all tab
		self.tabs.setTabsClosable(True) #set tabs closable
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab) #you can connect it to a any fuction you made
		
		# Button  widject
		self.button = QPushButton('Add Plot') #make button
		self.button.clicked.connect(self.getItem) #connect to getitem function

		# linedit widget
		self.le = QLineEdit(self) #make linedit
		self.le.textChanged.connect(self.refine) #convert text to arbic
		self.completer = QCompleter() #make autocompleter
		self.completer.setModel(QStringListModel(self.List)) #add List of stock to completer
		self.le.setCompleter(self.completer) #connect copmpleter to linedit
		self.le.returnPressed.connect(self.pushButtonOK) #connect to pushButtonOK function after press ENTER

	# Initialize main figure and layout
		# figure property
		self.resize(800, 600) #defult scheme size
		self.setWindowTitle('QTrader') #Window title

		# set layouts
		self.Vlayout = QVBoxLayout()
		self.Vlayout.addWidget(self.tabs)
		self.Hlayout = QHBoxLayout()
		self.Hlayout.addWidget(self.button)
		self.Hlayout.addWidget(self.le)
		self.Vlayout.addLayout(self.Hlayout)
		self.setLayout(self.Vlayout)

	def getItem(self): #input dialog for self.button
		item, ok = QInputDialog.getItem(
			self, "select input dialog", "list of languages", self.List, 0, False)
			
		if ok and item:
			stockname = Persian(item)
			self.le.setText(item)
			self.plot(stockname)

	def refine(self): #refine entry text in self.le
		stockname = Persian(self.le.text())
		self.le.setText(stockname)

	def pushButtonOK(self): #call self.plot function
		stockname = Persian(self.le.text())
		if stockname in self.List:
			self.plot(stockname)

	def plot(self, stockname, Bars=300): #open new tab and plot on it
		self.tabs.setCurrentIndex(self.tabs.addTab(
			Plot_Panel(stockname, self.get_data(stockname)), stockname))
	
	def get_data(self, stockname): #extarct history from database
		if not self.cursor.execute(
				"SELECT * FROM sqlite_master WHERE name = 'NAMAD'".replace('NAMAD', stockname)).fetchone():
			Get_Csv(id2stock(stockname))# if history not exit in data base download it
        
		elif self.cursor.execute(
 				"SELECT * FROM NAMAD LIMIT 1".replace('NAMAD', stockname)).fetchone()[0]!=int(date.today().strftime('%Y%m%d')):
			Get_Csv(id2stock(stockname)) #if data exist but not uptodate update it
				
		self.cursor.execute(
				'SELECT * FROM NAMAD ORDER BY Date ASC'.replace('NAMAD', stockname)) #get and sort data ascendig; 0 index has oldest date. [20161017, 20161018, ..., 20190413]
		data = np.array(self.cursor.fetchall(), int) #store data in numpy array with int format
		for i in range(len(data)): #turn date to matplotlib datatime format
			data[i][0] = mdates.date2num(
				dt.datetime.strptime(str(data[i][0]), '%Y%m%d'))

		return data

def main():
	app = QApplication(sys.argv)
	ex = Window('StockData.db')
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
