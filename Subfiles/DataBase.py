import requests, sqlite3

#Functions to interact with database: update, changes, manipulations and ....

def Persian(text, P=False):
    #persian charachter to arabic and vise versa,
    #to set a standard between tsetmc and my program;
	if P:
		# Arabic 2 Persian 
		Text = text.replace('ي','ی')
		Text = Text.replace('ك','ک')
	else:
		# Persian 2 Arabic
		Text = text.replace('ک', 'ك')
		Text = Text.replace('ی', 'ي')

	return Text

def UpdateDB():
	#this function update Stock view includs all stock
	#Extrct Data from tsetmc
	page = requests.get("http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0")
	t = page.content.decode().split('@')[2].split(';')

	#Open DataBase
	conn = sqlite3.connect('StockData.db')
	c = conn.cursor()

	# Insert rows of data
	for i in t:
		#Delet old data
		c.execute('DELETE FROM StockInfo WHERE Id='+i.split(',')[0]+';')
		#Make String
		#sample string: "25878262308375","IRO9GOLG0841","","61054",...,"13","9999.00","1.00","1000","311"
		STRING = 'INSERt INTO StockInfo VALUES ("'+ i.replace(',','","') +'");'
		#Add new data
		c.execute(STRING)

	# Save (commit) changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	return conn.close()
	
def Get_Csv(ID = '30703140537034664'):
	''' Give just Id'''
	#Give all history of a stock and put or update in database 
	#Extrct Data from tsetmc
	response = requests.get(
	    'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i='+ID+'&Top=999999&A=0')
	# sample respons: 20120509@1250@...@2590752@357;20120510@1265@...@256565@3987
	response = response.content.decode().split(';')[:-1]

	#Open DataBase
	conn = sqlite3.connect('StockData.db')
	c = conn.cursor()
	
	#creat stock table if it not exist
	STRING = '''
		CREATE TABLE IF NOT EXISTS NAMAD (
			Date	INEGER UNIQUE,
			Hight	INEGER,
			Low	INEGER,
			Payani	INEGER,
			Close	INEGER,
			Open	INEGER,
			yPayani	INEGER,
			Value	INEGER,
			Volume	INEGER,
			Number	INEGER
		)'''

	Namad = id2stock(ID,2)
	#sample table: CREATE TABLE IF NOT EXISTS "کگهر"
	c.execute(STRING.replace('NAMAD', '"'+Namad+'"'))
	#clear table for new data
	c.execute('DELETE FROM "NAMAD"'.replace('NAMAD',Namad))
	#put data in table
	for i in response:
		#sample string: INSERT INTO سامان VALUES ("20120509","1250",...,"2590752","357"))
		STRING = 'INSERT INTO "NAMAD" VALUES ("'+ i.replace('@','","') +'")'
		c.execute(STRING.replace('NAMAD',Namad))

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	return conn.close()

def id2stock(Id,inverse=0):
	conn = sqlite3.connect('StockData.db')
	c = conn.cursor()
	OutPut = c.execute('SELECT * FROM StockInfo')
	OutPut = OutPut.fetchall()

	for i in OutPut:
		if Id in i:
			return i[inverse]
