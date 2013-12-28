#!/usr/bin/python
# listbox.py

import wx
from fittopframe import FitTopFrame
from fitplotter import FitPlotter
from fitmainwindow import FitMainWindow
from topparser import top_dir_parser
import pandas as pd

class FitApp(wx.App):
    def OnInit(self):
        self.plotter= dict()
        self.top_window = FitMainWindow(None, wx.ID_ANY, 'FIT App')
        self.top_window.Center()
        self.top_window.Show(True)
        self.top_window.bind_launch_button(self.LaunchTopFrame)
        self.top_panel_dict = dict()
        self.top_total_data = pd.DataFrame()
        return True
        
    def LaunchTopFrame(self,event):
        self.top_frame = FitTopFrame(None, wx.ID_ANY, 'Top Window')
        self.top_frame.Centre()
        self.frames = dict()
        self.top_frame.bind_user_vs_param_summary_btn(self.UserVsParamSummary)
        self.top_frame.Show(True)
        return True
    
    def loadTopData(self):
        parsedir = self.top_window.get_current_dir()+'/'
        if not self.top_panel_dict:
            self.top_panel_dict=top_dir_parser(parsedir)
        
        if not self.top_total_data:
            self.top_total_data = pd.concat(self.top_panel_dict.values())

    def UserVsParamSummary(self, event):
        self.user_vs_param_summary_plotter = FitPlotter((2,2))
        self.plotter['uservsparam_summary'] = self.user_vs_param_summary_plotter
        self.loadTopData()
        grouped = self.top_total_data['RES'].groupby(self.top_total_data['USER'])
        self.user_vs_param_summary_plotter.grouped_plot(grouped.max(),1,'max')
        self.user_vs_param_summary_plotter.grouped_plot(grouped.min(),2,'min')
        self.user_vs_param_summary_plotter.grouped_plot(grouped.mean(),3,'mean')
        self.user_vs_param_summary_plotter.grouped_plot(grouped.std(),4,'std')
        self.user_vs_param_summary_plotter.Center()
        self.user_vs_param_summary_plotter.Show(True)

        return True


fit_app = FitApp(0)
fit_app.MainLoop()
