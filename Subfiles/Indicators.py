from Subfiles.Classes import *

class WesternCandlestick(QGraphicsObject): #make WesternCandlestick QGraphicsObject for plot price history
	# order data: time, open, close, min, max
	def __init__(self, data):
		QGraphicsObject.__init__(self)
		self.data = data  #data must have fields: time, Hight, Low, payani, close, Open
		self.generatePicture() #generate picture

	def generatePicture(self):
		## pre-computing a QPicture object allows paint() to run much more quickly, 
		## rather than re-drawing the shapes every time.
				
		OFFSET = .4
		self.picture = QPicture()
		p = QPainter(self.picture)
		p.setPen(pg.mkPen('c',width=2))

		Date, Hight, Low, payani, Close, Open = self.data[0]
		p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
#		p.drawLine(QPointF(Date, payani), QPointF(Date+OFFSET, payani))
		p.drawLine(QPointF(Date, Close), QPointF(Date+OFFSET, Close))
		p.drawLine(QPointF(Date-OFFSET, Open), QPointF(Date, Open))
		PreviousBar = payani

		for (Date, Hight, Low, payani, Close, Open) in self.data[1:]:
#			p.setPen(pg.mkPen('y',width=2))
#			p.drawLine(QPointF(Date, payani), QPointF(Date+OFFSET, payani))
			p.setPen(pg.mkPen('y',width=.5,style=Qt.DotLine))
			p.drawLine(QPointF(Date-OFFSET, int(1.05*PreviousBar)), QPointF(Date+OFFSET, int(1.05*PreviousBar)))
			p.drawLine(QPointF(Date-OFFSET, ceil(.95*PreviousBar)), QPointF(Date+OFFSET, ceil(.95*PreviousBar)))
			p.drawLine(QPointF(Date, ceil(.95*PreviousBar)), QPointF(Date, int(1.05*PreviousBar)))

			p.setPen(pg.mkPen(['r','g'][PreviousBar < Close],width=2))
			p.drawLine(QPointF(Date, Low), QPointF(Date, Hight))
			p.drawLine(QPointF(Date, Close), QPointF(Date+OFFSET, Close))
			p.drawLine(QPointF(Date-OFFSET, Open), QPointF(Date, Open))
			
			PreviousBar = payani
		p.end()

	def paint(self, p, *args):
		p.drawPicture(0, 0, self.picture)

	def boundingRect(self):
		## boundingRect _must_ indicate the entire area that will be drawn on
		## or else we will get artifacts and possibly crashing.
		## (in this case, QPicture does all the work of computing the bouning rect for us)

		return QRectF(self.picture.boundingRect())

class Payani(QGraphicsObject): #make Payani Indicator for plot price history

	def __init__(self, data):
		QGraphicsObject.__init__(self)
		self.data = data  #data must have fields: time, payani
		self.generatePicture() #generate picture

	def generatePicture(self):
		## pre-computing a QPicture object allows paint() to run much more quickly, 
		## rather than re-drawing the shapes every time.
				
		OFFSET = .4
		self.picture = QPicture()
		p = QPainter(self.picture)
		p.setPen(pg.mkPen('y',width=2))

		for (Date, payani) in self.data: p.drawLine(QPointF(Date, payani), QPointF(Date+OFFSET, payani))
		p.end()

	def paint(self, p, *args):
		p.drawPicture(0, 0, self.picture)

	def boundingRect(self):
		## boundingRect _must_ indicate the entire area that will be drawn on
		## or else we will get artifacts and possibly crashing.
		## (in this case, QPicture does all the work of computing the bouning rect for us)

		return QRectF(self.picture.boundingRect())

