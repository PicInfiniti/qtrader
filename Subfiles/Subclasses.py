#this file include utility classes
import pyqtgraph as pg
import matplotlib.dates as mdates
import jdatetime as jdt

class TimeAxisItem(pg.AxisItem): #show time in ratioanl way
    def __init__(self,*args, **kwargs):
        super(TimeAxisItem,self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [jdt.date.fromgregorian(date=mdates.num2date(value)) for value in values] #persian date
        #return [mdates.num2date(value).strftime('%Y-%m-%d') for value in values] #milady date

