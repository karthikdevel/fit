import os

import wx
import wx.calendar as wxcal
from fittopframe import FitTopFrame

class FitMainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (250, 150))

        self.start_date = ""
        self.end_date = ""
        self.setEpochEternal()

        self.SetMinSize((750, 300))
        self.Center()

        self.panel = wx.Panel(self, -1)

        # top level sizer.
        self.main_grid_bag_sizer = wx.GridBagSizer(9,9)

        self.dir_name = wx.TextCtrl(self.panel, wx.ID_ANY, size=(180, 20))
        self.dir_name.SetValue("Enter")
        self.log_path = wx.Button(self.panel, wx.ID_ANY, "Logs Path")
        self.log_path.Bind(wx.EVT_BUTTON, self.openDir)

        # Check grid_bag to select Top/Free/IOStat
        self.top_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Top')
        self.top_cb.SetValue(False)
        self.free_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Free')
        self.free_cb.SetValue(False)

        self.launch_button = wx.Button(self.panel, wx.ID_ANY, "Launch")
        self.launch_button.Bind(wx.EVT_BUTTON,self.LaunchTopFrame)

        self.start_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Start Date")
        self.start_static_box_sizer = wx.StaticBoxSizer(self.start_static_box,wx.VERTICAL)
        self.end_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "End Date")
        self.end_static_box_sizer = wx.StaticBoxSizer(self.end_static_box,wx.VERTICAL)        

        self.start_cal = wxcal.CalendarCtrl(self.panel, wx.ID_ANY, wx.DateTime.Today(),
                                            style=wxcal.CAL_SEQUENTIAL_MONTH_SELECTION)

        self.start_cal.Bind(wxcal.EVT_CALENDAR_SEL_CHANGED,self.SetStart)


        self.end_cal = wxcal.CalendarCtrl(self.panel, wx.ID_ANY, wx.DateTime.Today(),
                                          style=wxcal.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.end_cal.Bind(wxcal.EVT_CALENDAR_SEL_CHANGED,self.SetEnd)

        self.start_static_box_sizer.Add(self.start_cal, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.end_static_box_sizer.Add(self.end_cal, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        self.end_cal.Disable()
        self.start_cal.Disable()        

        self.date_sel = wx.CheckBox(self.panel, wx.ID_ANY, 'Date Range')
        self.date_sel.SetValue(False)
        self.date_sel.Bind(wx.EVT_CHECKBOX, self.calenderEnDis)

        # Add to the correct grid_bag.
        self.main_grid_bag_sizer.Add(self.dir_name, pos=(0,0), span=(1,3), flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.log_path, (0,3), (1,1), flag = wx.EXPAND)        
        self.main_grid_bag_sizer.Add(self.launch_button, (1,3), (1,1), flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.top_cb, (1,0), (1,1),flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.free_cb, (1,1), (1,1), flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.start_static_box_sizer, (2,0),wx.DefaultSpan,flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.end_static_box_sizer, (2,1),wx.DefaultSpan, flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.date_sel, (2,3), (1,1), flag = wx.EXPAND)

        self.panel.SetSizerAndFit(self.main_grid_bag_sizer)

    def calenderEnDis(self, event):
        cb = event.GetEventObject()
        if  cb.GetValue() == True:
            self.end_cal.Enable()
            self.start_cal.Enable()
        else:
            self.end_cal.Disable()
            self.start_cal.Disable()
            self.setEpochEternal()

    def setEpochEternal(self):
        dt = wx.DateTime().Set(day=1,month=1,year=1900)
        self.start_date = str(dt)
        dt.Set(day=1,month=1,year=2050)
        self.end_date = str(dt)

    def SetStart(self, event):
        self.start_date = str(event.GetDate())

    def SetEnd(self, event):        
        self.end_date = str(event.GetDate())

    def openDir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_name.SetValue(dlg.GetPath())
        dlg.Destroy()

    def LaunchTopFrame(self,event):
        if os.path.exists(self.dir_name.GetValue()) == True:
            self.top_frame = FitTopFrame(None, wx.ID_ANY, self.dir_name.GetValue(), self.start_date, self.end_date, title='Top Window')
            self.top_frame.Centre(True)
            self.frames = dict()
            self.top_frame.Show(True)
        else:
            self.showErrorDialog("Directory does not exist.")

    def showErrorDialog(self, message, closeFrame = False):
        dia = wx.MessageDialog(self, message, 'Error', style = wx.OK|wx.ICON_ERROR)
        dia.ShowModal()
        if closeFrame == True:
            self.Destroy()
        else:
            dia.Destroy()
