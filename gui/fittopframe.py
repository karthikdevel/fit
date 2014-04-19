import wx
import os
import threading
import pandas as pd
import numpy as np
import Queue

from fitplotter import FitPlotter
from  parser.topparser import TopDirParser
from fitlistbox import FitListBox


class FitTopFrame(wx.Frame):
    def __init__(self, parent, id, parsedir, start_date, end_date, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (750, 450))

        self.SetMinSize((750, 450))
        self.Center(True)

        self.parsedir = parsedir
        self.plotter = dict()

        self.top_dir_parser = self.loadTopData(start_date, end_date)
        if self.top_dir_parser == None:
            self.Destroy()
            return

        self.user_list = self.top_dir_parser.GetItemList('USER')
        self.process_list = self.top_dir_parser.GetItemList('COMMAND')
        self.params_list = ['RES','%CPU']

        if self.user_list == None or self.process_list == None:
            self.showErrorDialog('No User/Process -- Please check directory/Date Range', True)
            return

        self.panel = wx.Panel(self, -1)

        # top level sizer.
        self.main_grid_sizer = wx.GridSizer(2,3,5,10)

        # Static box for each list box
        user_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "User List")
        self.user_static_box_sizer = wx.StaticBoxSizer(user_static_box,wx.VERTICAL)
        process_static_box = wx.StaticBox(self.panel, wx.ID_ANY, label="Process List")
        self.process_listbox_sizer = wx.StaticBoxSizer(process_static_box,wx.VERTICAL)
        param_static_box = wx.StaticBox(self.panel, wx.ID_ANY, label="Param List")
        self.param_listbox_sizer = wx.StaticBoxSizer(param_static_box,wx.VERTICAL)

        # User List Box
        self.user_listbox = FitListBox(self.panel, wx.ID_ANY,
                                       wx.DefaultPosition, (170, 130), self.user_list, wx.LB_MULTIPLE |
                                       wx.LB_SORT)
        self.user_listbox.SetSelection(0)
        # Check Box to select all users
        self.all_user_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Select All')
        self.all_user_cb.SetValue(False)
        self.all_user_cb.Bind(wx.EVT_CHECKBOX, self.toggleAllUserSelect)

        # Process List Box
        self.process_listbox = FitListBox(self.panel, wx.ID_ANY,
                                          wx.DefaultPosition, (170, 130), self.process_list, wx.LB_MULTIPLE |
                                          wx.LB_SORT)
        self.process_listbox.SetSelection(0)

        # Check Box to select all processes
        self.all_process_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Select All')
        self.all_process_cb.SetValue(False)
        self.all_process_cb.Bind(wx.EVT_CHECKBOX, self.toggleAllProcessSelect)

        # Param List Box
        self.param_listbox = FitListBox(self.panel, wx.ID_ANY,
                                        wx.DefaultPosition, (170, 130), self.params_list, wx.LB_SINGLE)
        self.param_listbox.SetSelection(0)

        self.user_static_box_sizer.Add(self.user_listbox, proportion = 1,
                                       flag = wx.ALL | wx.EXPAND, border = 10)
        self.user_static_box_sizer.Add(self.all_user_cb, 0, wx.BOTTOM | wx.CENTER)
        self.process_listbox_sizer.Add(self.process_listbox, proportion = 1,
                                       flag = wx.ALL | wx.EXPAND, border = 10)
        self.process_listbox_sizer.Add(self.all_process_cb, 0, wx.BOTTOM | wx.CENTER)
        self.param_listbox_sizer.Add(self.param_listbox, proportion = 1, flag
                                     = wx.ALL | wx.EXPAND, border = 10)

        # Add Each list box to main grid sizer.
        self.main_grid_sizer.Add(self.user_static_box_sizer, proportion = 1,
                                 flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.main_grid_sizer.Add(self.process_listbox_sizer, proportion = 1,
                                 flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.main_grid_sizer.Add(self.param_listbox_sizer, proportion = 1,
                                 flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        # Static box for each type of plot (Summary,Time plots & Scatter plots)
        summary_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Summary")
        self.summary_plot_static_box_sizer  = wx.StaticBoxSizer(summary_plot_static_box, wx.VERTICAL)

        time_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Time")
        self.time_plot_static_box_sizer = wx.StaticBoxSizer(time_plot_static_box,wx.VERTICAL)

        scatter_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Scatter")
        self.scatter_plot_static_box_sizer = wx.StaticBoxSizer(scatter_plot_static_box,wx.VERTICAL)

        # Buttons for each type of plot.
        self.user_vs_param_summary_btn = wx.Button(self.panel, wx.ID_ANY, 'User(s) vs Param')
        self.user_vs_param_summary_btn.Bind(wx.EVT_BUTTON, self.userVsParamSummary)
        self.process_vs_param_summary_btn = wx.Button(self.panel, wx.ID_ANY, 'Process(s) vs Param')
        self.process_vs_param_summary_btn.Bind(wx.EVT_BUTTON, self.processVsParamSummary)

        self.summary_plot_static_box_sizer.Add(self.user_vs_param_summary_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.summary_plot_static_box_sizer.Add(self.process_vs_param_summary_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        self.peruserparam_vs_time_btn = wx.Button(self.panel, wx.ID_ANY, 'Time vs per User Param')
        self.peruserparam_vs_time_btn.Bind(wx.EVT_BUTTON, self.perUserParamVsTime)
        self.enable_user_locall_sum = wx.CheckBox(self.panel, wx.ID_ANY, 'Selected Total')
        self.enable_user_locall_sum.SetValue(False)        
        self.perprocessparam_vs_time_btn = wx.Button(self.panel, wx.ID_ANY, 'Time vs per Process Param')
        self.perprocessparam_vs_time_btn.Bind(wx.EVT_BUTTON, self.perProcessParamVsTime)
        self.enable_process_locall_sum = wx.CheckBox(self.panel, wx.ID_ANY, 'Selected Total')
        self.enable_process_locall_sum.SetValue(False)

        self.time_plot_static_box_sizer.Add(self.peruserparam_vs_time_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.time_plot_static_box_sizer.Add(self.enable_user_locall_sum, 0, flag = wx.RIGHT | wx.CENTER)
        self.time_plot_static_box_sizer.Add(self.perprocessparam_vs_time_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.time_plot_static_box_sizer.Add(self.enable_process_locall_sum, 0, flag = wx.RIGHT | wx.CENTER)

        self.user_vs_process_btn = wx.Button(self.panel, wx.ID_ANY, 'User vs Process')

        self.scatter_plot_static_box_sizer.Add(self.user_vs_process_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        # Add each plot category to the correct grid.
        self.main_grid_sizer.Add(self.summary_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        self.main_grid_sizer.Add(self.time_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        self.main_grid_sizer.Add(self.scatter_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.panel.SetSizerAndFit(self.main_grid_sizer)

    def loadTopData(self, start, end):
        self.parsedir = self.parsedir+'/'
        file_list= os.listdir(self.parsedir)
        self.numfiles_in_range = 0
        
        #Find number of files in range for progress bar.
        for ifile in file_list:
            fs = pd.to_datetime(ifile[:ifile.find('.')])
            if fs >= pd.to_datetime(start) and fs <= pd.to_datetime(end):
                self.numfiles_in_range += 1
                
        parser = TopDirParser(start, end, self.parsedir)

        self.files_loaded = 0

        self.progressDialog = wx.ProgressDialog("Loading Data",
                                       "Starting Data Load...",
                                       maximum = self.numfiles_in_range,
                                       parent = self,
                                       style = wx.PD_APP_MODAL
                                        | wx.PD_CAN_ABORT
                                        | wx.PD_AUTO_HIDE
                                        | wx.PD_ELAPSED_TIME
                                        | wx.PD_ESTIMATED_TIME
                                        | wx.PD_REMAINING_TIME
                                        )

        queue = Queue.Queue()
        parserThread = threading.Thread(target=parser.LoadData,
                                        args=(self.progressDialog, queue,
                                              self.numfiles_in_range) )
        parserThread.setDaemon(True)
        parserThread.start()        
        self.progressDialog.ShowModal()
        
        parserThread.join()
        self.files_loaded = queue.get()
        
        if self.files_loaded == self.numfiles_in_range:
            return parser
        else:
            return None
        

    def showErrorDialog(self,message, closeFrame = False):
        dia = wx.MessageDialog(self, message, 'Error', style = wx.OK|wx.ICON_ERROR)
        dia.ShowModal()
        if closeFrame == True:
            self.Destroy()
        else:
            dia.Destroy()

        return

    def checkEmpty(self, obj, message):
        if obj.empty:
            self.showErrorDialog(message)
            return True
        else:
            return False

    def checkSelectionsEmpty(self):
        if len(self.user_listbox.GetSelections()) == 0:
            self.showErrorDialog("No user selected")
            return True
        elif len(self.process_listbox.GetSelections()) == 0:
            self.showErrorDialog("No process selected")
            return True
        else:
            return False

    def userVsParamSummary(self, event):
        if self.checkSelectionsEmpty() == True:
            return
        preselector={'COMMAND':self.process_listbox.GetSelList(self.process_list)}
        df = self.top_dir_parser.GenDF('USER',False,preselector)
        drop_list = self.param_listbox.GetDropList(self.params_list)
        df = df.drop(drop_list,level=1)
        drop_list = self.user_listbox.GetDropList(self.user_list)
        for i in drop_list[:]:
            if i not in df.index:
                drop_list.remove(i)
        df = df.drop(drop_list)
        if self.checkEmpty(df, "Empty Data") == True:
            return
        self.user_vs_param_summary_plotter = FitPlotter((2,2))
        self.plotter['uservsparam_summary'] = self.user_vs_param_summary_plotter        
        ser = df.transpose().max().reset_index('minor').drop('minor',axis=1)
        self.user_vs_param_summary_plotter.grouped_plot(ser,1,'max')
        ser = df.transpose().min().reset_index('minor').drop('minor',axis=1)
        self.user_vs_param_summary_plotter.grouped_plot(ser,2,'min')
        ser = df.transpose().mean().reset_index('minor').drop('minor',axis=1)
        self.user_vs_param_summary_plotter.grouped_plot(ser,3,'mean')
        ser = df.transpose().std().reset_index('minor').drop('minor',axis=1)
        self.user_vs_param_summary_plotter.grouped_plot(ser,4,'std')
        self.user_vs_param_summary_plotter.Center()
        self.user_vs_param_summary_plotter.Show(True)

    def perUserParamVsTime(self, event):
        if self.checkSelectionsEmpty() == True:
            return        
        preselector={'COMMAND':self.process_listbox.GetSelList(self.process_list)}
        df,gd = self.top_dir_parser.GenDF('USER',True,preselector)
        drop_list = self.param_listbox.GetDropList(self.params_list)
        df = df.drop(drop_list,level=1)
        drop_list = self.user_listbox.GetDropList(self.user_list)
        for i in drop_list[:]:
            if i not in df.index:
                drop_list.remove(i)        
        df = df.drop(drop_list)
        if self.checkEmpty(df, "Empty Data") == True:
            return
        self.userparam_vs_time_plotter = FitPlotter((1,1))
        self.plotter['userparamvstime'] = self.userparam_vs_time_plotter        
        self.userparam_vs_time_plotter.simple_plot(df.transpose(),title="UserMem Vs Time")
        if self.enable_user_locall_sum.GetValue() == True:
            self.userparam_vs_time_plotter.simple_plot(df.sum(),label='Selected Total', style = '--',color='r')
        self.userparam_vs_time_plotter.simple_plot(gd,label='Global Total', style = '--',color='g')
        self.userparam_vs_time_plotter.Center()
        self.userparam_vs_time_plotter.Show(True)

    def processVsParamSummary(self, event):
        if self.checkSelectionsEmpty() == True:
            return        
        preselector={'USER':self.user_listbox.GetSelList(self.user_list)}
        df = self.top_dir_parser.GenDF('COMMAND',False,preselector)
        drop_list = self.param_listbox.GetDropList(self.params_list)
        df = df.drop(drop_list,level=1)
        drop_list = self.process_listbox.GetDropList(self.process_list)
        for i in drop_list[:]:
            if i not in df.index:
                drop_list.remove(i)
        df = df.drop(drop_list)
        if self.checkEmpty(df, "Empty Data") == True:
            return
        self.process_vs_param_summary_plotter = FitPlotter((2,2))
        self.plotter['processvsparam_summary'] = self.process_vs_param_summary_plotter        
        ser = df.transpose().max().reset_index('minor').drop('minor',axis=1)
        self.process_vs_param_summary_plotter.grouped_plot(ser,1,'max')
        ser = df.transpose().min().reset_index('minor').drop('minor',axis=1)
        self.process_vs_param_summary_plotter.grouped_plot(ser,2,'min')
        ser = df.transpose().mean().reset_index('minor').drop('minor',axis=1)
        self.process_vs_param_summary_plotter.grouped_plot(ser,3,'mean')
        ser = df.transpose().std().reset_index('minor').drop('minor',axis=1)
        self.process_vs_param_summary_plotter.grouped_plot(ser,4,'std')
        self.process_vs_param_summary_plotter.Center()
        self.process_vs_param_summary_plotter.Show(True)

    def perProcessParamVsTime(self, event):
        if self.checkSelectionsEmpty() == True:
            return        
        preselector={'USER':self.user_listbox.GetSelList(self.user_list)}
        df,gd = self.top_dir_parser.GenDF('COMMAND',True,preselector)
        drop_list = self.param_listbox.GetDropList(self.params_list)
        df = df.drop(drop_list,level=1)
        drop_list = self.process_listbox.GetDropList(self.process_list)
        for i in drop_list[:]:
            if i not in df.index:
                drop_list.remove(i)        
        df = df.drop(drop_list)
        if self.checkEmpty(df, "Empty Data") == True:
            return
        self.processparam_vs_time_plotter = FitPlotter((1,1))
        self.plotter['processparamvstime'] = self.processparam_vs_time_plotter        
        self.processparam_vs_time_plotter.simple_plot(df.transpose(),title="ProcessMem Vs Time")
        if self.enable_process_locall_sum.GetValue() == True:
            self.processparam_vs_time_plotter.simple_plot(df.sum(),label='Selected Total', style = '--',color='r')
        self.processparam_vs_time_plotter.simple_plot(gd,label='Global Total', style = '--',color='g')        
        self.processparam_vs_time_plotter.Center()
        self.processparam_vs_time_plotter.Show(True)

        return

    def toggleAllUserSelect(self, event):
        if self.all_user_cb.GetValue() == True:
            for i in range(self.user_listbox.GetCount()):
                self.user_listbox.SetSelection(i)
        else:
            for i in range(self.user_listbox.GetCount()):
                self.user_listbox.Deselect(i)
            self.user_listbox.SetSelection(0)

        return True

    def toggleAllProcessSelect(self, event):
        if self.all_process_cb.GetValue() == True:
            for i in range(self.process_listbox.GetCount()):
                self.process_listbox.SetSelection(i)
        else:
            for i in range(self.process_listbox.GetCount()):
                self.process_listbox.Deselect(i)
            self.process_listbox.SetSelection(0)

        return True
