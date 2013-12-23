#!/usr/bin/python
# listbox.py

import wx

class FitTopFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (750, 450))

        self.SetMinSize((750, 450))

        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(wx.ID_ANY,  'Quit', '' )
        menubar.Append(file, "&File")
        self.SetMenuBar(menubar)

        self.user_list = ['shanmuk','raji','karthik','prathi']
        self.process_list = ['Novas','vim', 'python']
        self.params_list = ['mem','CPU']

        self.panel = wx.Panel(self, -1)

        # top level sizer.
        self.main_grid_sizer = wx.GridSizer(2,3,5,10)

        # Static box for each list box
        user_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "User List")
        self.user_static_box = wx.StaticBoxSizer(user_static_box,wx.VERTICAL)
        process_static_box = wx.StaticBox(self.panel, wx.ID_ANY, label="Process List")
        self.process_listbox_sizer = wx.StaticBoxSizer(process_static_box,wx.VERTICAL)
        param_static_box = wx.StaticBox(self.panel, wx.ID_ANY, label="Param List")
        self.param_listbox_sizer = wx.StaticBoxSizer(param_static_box,wx.VERTICAL)

        # User List Box
        self.user_listbox = wx.ListBox(self.panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.user_list, wx.LB_MULTIPLE)
        self.user_listbox.SetSelection(0)
        # Check Box to select all users
        self.all_user_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Select All')
        self.all_user_cb.SetValue(False)
        self.all_user_cb.Bind(wx.EVT_CHECKBOX, self.toggleAllUserSelect)

        # Process List Box
        self.process_listbox = wx.ListBox(self.panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.process_list, wx.LB_MULTIPLE)
        self.process_listbox.SetSelection(0)
        # Check Box to select all processes
        self.all_process_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Select All')
        self.all_process_cb.SetValue(False)
        self.all_process_cb.Bind(wx.EVT_CHECKBOX, self.toggleAllProcessSelect)

        # Param List Box
        self.param_listbox = wx.ListBox(self.panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.params_list, wx.LB_SINGLE)
        self.param_listbox.SetSelection(0)

        self.user_static_box.Add(self.user_listbox, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.user_static_box.Add(self.all_user_cb, 0, wx.BOTTOM | wx.CENTER)
        self.process_listbox_sizer.Add(self.process_listbox, proportion = 1,  flag = wx.ALL | wx.EXPAND, border = 10)
        self.process_listbox_sizer.Add(self.all_process_cb, 0, wx.BOTTOM | wx.CENTER)
        self.param_listbox_sizer.Add(self.param_listbox, proportion = 1,  flag = wx.ALL | wx.EXPAND, border = 10)

        # Add Each list box to main grid sizer.
        self.main_grid_sizer.Add(self.user_static_box, proportion = 1,  flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.main_grid_sizer.Add(self.process_listbox_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.main_grid_sizer.Add(self.param_listbox_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        # Static box for each type of plot (Summary,Time plots & Scatter plots)
        summary_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Summary")
        self.summary_plot_static_box_sizer  = wx.StaticBoxSizer(summary_plot_static_box, wx.VERTICAL)

        time_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Time")
        self.time_plot_static_box_sizer = wx.StaticBoxSizer(time_plot_static_box,wx.VERTICAL)

        scatter_plot_static_box = wx.StaticBox(self.panel, wx.ID_ANY, "Scatter")
        self.scatter_plot_static_box_sizer = wx.StaticBoxSizer(scatter_plot_static_box,wx.VERTICAL)

        # Buttons for each type of plot.
        self.user_vs_param_summary_btn = wx.Button(self.panel, wx.ID_ANY, 'User(s) vs Param')
        self.process_vs_param_summary_btn = wx.Button(self.panel, wx.ID_ANY, 'Process(s) vs Param')

        self.summary_plot_static_box_sizer.Add(self.user_vs_param_summary_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.summary_plot_static_box_sizer.Add(self.process_vs_param_summary_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        self.peruserparam_vs_time_btn = wx.Button(self.panel, wx.ID_ANY, 'Time vs per User Param')
        self.perprocessparam_vs_time_btn = wx.Button(self.panel, wx.ID_ANY, 'Time vs per Process Param')

        self.time_plot_static_box_sizer.Add(self.peruserparam_vs_time_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)
        self.time_plot_static_box_sizer.Add(self.perprocessparam_vs_time_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        self.user_vs_process_btn = wx.Button(self.panel, wx.ID_ANY, 'User vs Process')

        self.scatter_plot_static_box_sizer.Add(self.user_vs_process_btn, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 10)

        # Add each plot category to the correct grid.
        self.main_grid_sizer.Add(self.summary_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        self.main_grid_sizer.Add(self.time_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)
        self.main_grid_sizer.Add(self.scatter_plot_static_box_sizer, proportion = 1, flag = wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        self.panel.SetSizerAndFit(self.main_grid_sizer)

    def toggleAllUserSelect(self, event):
        if self.all_user_cb.GetValue() == True:
            for i in range(self.user_listbox.GetCount()):
                self.user_listbox.SetSelection(i)
        else:
            for i in range(self.user_listbox.GetCount()):
                self.user_listbox.Deselect(i)
            self.user_listbox.SetSelection(0)

    def toggleAllProcessSelect(self, event):
        if self.all_process_cb.GetValue() == True:
            for i in range(self.process_listbox.GetCount()):
                self.process_listbox.SetSelection(i)
        else:
            for i in range(self.process_listbox.GetCount()):
                self.process_listbox.Deselect(i)
            self.process_listbox.SetSelection(0)

class FitApp(wx.App):
    def OnInit(self):
        frame = FitTopFrame(None, wx.ID_ANY, 'listbox.py')
        frame.Centre()
        frame.Show(True)
        return True

fit_app = FitApp(0)
fit_app.MainLoop()
