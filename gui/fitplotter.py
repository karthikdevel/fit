import wx
from numpy import arange, sin, pi
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class FitPlotter(wx.Frame):
    def __init__(self,subplots):
        wx.Frame.__init__(self, None, wx.ID_ANY, title= 'Summary - User Vs Param',pos=(350,300),size=(700, 700))
        self.SetMinSize((700,700))
        #self.Center()


        self.panel=wx.Panel(self, wx.ID_ANY)
        
        self.figure = Figure()
        self.max_subplots = subplots[0]*subplots[1]
        self.axes = [self.figure.add_subplot(subplots[0],subplots[1],i) for i in range(1,self.max_subplots+1)]
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        # instantiate the Navigation Toolbar
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        # needed to support Windows systems
        #self.toolbar.Realize()
        # add it to the sizer
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # explicitly show the toolbar
        self.toolbar.Show()
        self.panel.SetSizerAndFit(self.sizer)

    def grouped_plot(self,plottable,subplot,title):
        if subplot <= self.max_subplots:
            plottable.plot(kind='bar',ax=self.axes[subplot-1],title=title)
        else:
            return False
        
    def simple_plot(self,plottable,title):
        plottable.plot(ax=self.axes[0],title=title)

