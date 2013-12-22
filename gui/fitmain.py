#!/usr/bin/python
# listbox.py

import wx

class FitTopFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (750, 450))

        self.SetMinSize((750, 450))

        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, 'Quit', '' )
        menubar.Append(file, "&File")
        self.SetMenuBar(menubar)

        self.user_list = ['shanmuk','raji']
        self.process_list = ['Novas','vim']
        self.params_list = ['mem','CPU']

        panel = wx.Panel(self, -1)
        
        # top level sizer.
        main_grid_sizer = wx.GridSizer(2,3,5,10)

        # Static box for each list box
        user_static_box= wx.StaticBox(panel, -1, "User List")
        user_listbox_sizer = wx.StaticBoxSizer(user_static_box,wx.VERTICAL)
        process_static_box= wx.StaticBox(panel, -1, label="Process List")
        process_listbox_sizer = wx.StaticBoxSizer(process_static_box,wx.VERTICAL)
        param_static_box= wx.StaticBox(panel, -1, label="Param List")
        param_listbox_sizer = wx.StaticBoxSizer(param_static_box,wx.VERTICAL)

        # User List Box
        self.user_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.user_list, wx.LB_MULTIPLE)
        self.user_listbox.SetSelection(0)
        # Check Box to select all users
        self.all_user_cb = wx.CheckBox(panel, wx.ID_ANY, 'Select All')
        self.all_user_cb.SetValue(False)

        # Process List Box
        self.process_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.process_list, wx.LB_MULTIPLE)
        self.process_listbox.SetSelection(0)
        # Check Box to select all processes
        self.all_process_cb = wx.CheckBox(panel, wx.ID_ANY, 'Select All')
        self.all_process_cb.SetValue(False)

        # Param List Box
        self.param_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.params_list, wx.LB_SINGLE)
        self.param_listbox.SetSelection(0)

        user_listbox_sizer.Add(self.user_listbox, 1,wx.ALL | wx.EXPAND, border = 10)
        user_listbox_sizer.Add(self.all_user_cb,0, wx.BOTTOM | wx.CENTER)
        process_listbox_sizer.Add(self.process_listbox, 1, wx.ALL | wx.EXPAND, border = 10)
        process_listbox_sizer.Add(self.all_process_cb,0, wx.BOTTOM | wx.CENTER)
        param_listbox_sizer.Add(self.param_listbox, 1, wx.ALL | wx.EXPAND, border = 10)

        # Add Each list box to main grid sizer.
        main_grid_sizer.Add(user_listbox_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        main_grid_sizer.Add(process_listbox_sizer, 1,wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        main_grid_sizer.Add(param_listbox_sizer, 1,wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        
        # Static box for each type of plot (Summary,Time plots & Scatter plots)
        summary_plot_static_box= wx.StaticBox(panel, -1, "Summary")
        summary_plot_buttons_sizer = wx.StaticBoxSizer(summary_plot_static_box,wx.VERTICAL)

        time_plot_static_box= wx.StaticBox(panel, -1, "Time")
        time_plot_buttons_sizer = wx.StaticBoxSizer(time_plot_static_box,wx.VERTICAL)

        scatter_plot_static_box= wx.StaticBox(panel, -1, "Scatter")
        scatter_plot_buttons_sizer = wx.StaticBoxSizer(scatter_plot_static_box,wx.VERTICAL)
        
        # Buttons for each type of plot.
        self.user_vs_param_summary_btn = wx.Button(panel, wx.ID_ANY, 'User(s) vs Param')
        self.process_vs_param_summary_btn = wx.Button(panel, wx.ID_ANY, 'Process(s) vs Param')

        summary_plot_buttons_sizer.Add(self.user_vs_param_summary_btn, 1,wx.ALL | wx.EXPAND, border = 10)
        summary_plot_buttons_sizer.Add(self.process_vs_param_summary_btn, 1,wx.ALL | wx.EXPAND, border = 10)        

        self.peruserparam_vs_time_btn = wx.Button(panel, wx.ID_ANY, 'Time vs per User Param')
        self.perprocessparam_vs_time_btn = wx.Button(panel, wx.ID_ANY, 'Time vs per Process Param')
        
        time_plot_buttons_sizer.Add(self.peruserparam_vs_time_btn, 1,wx.ALL | wx.EXPAND, border = 10)
        time_plot_buttons_sizer.Add(self.perprocessparam_vs_time_btn, 1,wx.ALL | wx.EXPAND, border = 10)

        self.user_vs_process_btn = wx.Button(panel, wx.ID_ANY, 'User vs Process')
        
        scatter_plot_buttons_sizer.Add(self.user_vs_process_btn, 1,wx.ALL | wx.EXPAND, border = 10)
        
        # Add each plot category to the correct grid.
        main_grid_sizer.Add(summary_plot_buttons_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        main_grid_sizer.Add(time_plot_buttons_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        main_grid_sizer.Add(scatter_plot_buttons_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        
        panel.SetSizerAndFit(main_grid_sizer)

class FitApp(wx.App):
    def OnInit(self):
        frame = FitTopFrame(None, -1, 'listbox.py')
        frame.Centre()
        frame.Show(True)
        return True

fit_app = FitApp(0)
fit_app.MainLoop()
