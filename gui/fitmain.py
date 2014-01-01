#!/usr/bin/python
# listbox.py

import wx

from fitmainwindow import FitMainWindow


class FitApp(wx.App):
    def OnInit(self):
        self.top_window = FitMainWindow(None, wx.ID_ANY, 'FIT App')
        self.top_window.Center()
        self.top_window.Show(True)
        return True
       

fit_app = FitApp(0)
fit_app.MainLoop()
