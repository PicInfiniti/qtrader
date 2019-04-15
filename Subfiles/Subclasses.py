#this file include utility classes
import pyqtgraph as pg
import matplotlib.dates as mdates

class TimeAxisItem(pg.AxisItem): #show time in ratioanl way
    def __init__(self,*args, **kwargs):
        super(TimeAxisItem,self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [mdates.num2date(value).strftime('%Y-%m-%d') for value in values]

