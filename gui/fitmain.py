#!/usr/bin/python
# listbox.py

import wx

class FitTopFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (750, 350))

        self.SetMinSize((750, 350))

        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, 'Quit', '' )
        menubar.Append(file, "&File")
        self.SetMenuBar(menubar)

        self.user_list = ['shanmuk','raji']
        self.process_list = ['Novas','vim']
        self.params_list = ['mem','CPU']

        panel = wx.Panel(self, -1)
        gs = wx.GridSizer(1,3,5,10)
        user_static_box= wx.StaticBox(panel, -1, "User List")
        user_listbox_sizer = wx.StaticBoxSizer(user_static_box,wx.VERTICAL)
        process_static_box= wx.StaticBox(panel, -1, label="Process List")
        process_listbox_sizer = wx.StaticBoxSizer(process_static_box,wx.VERTICAL)
        param_static_box= wx.StaticBox(panel, -1, label="Param List")
        param_listbox_sizer = wx.StaticBoxSizer(param_static_box,wx.VERTICAL)


        self.user_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.user_list, wx.LB_MULTIPLE)
        self.user_listbox.SetSelection(0)
        self.all_user_cb = wx.CheckBox(panel, wx.ID_ANY, 'Select All')
        self.all_user_cb.SetValue(False)


        self.process_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.process_list, wx.LB_MULTIPLE)
        self.process_listbox.SetSelection(0)
        self.all_process_cb = wx.CheckBox(panel, wx.ID_ANY, 'Select All')
        self.all_process_cb.SetValue(False)

        self.param_listbox = wx.ListBox(panel, wx.ID_ANY, wx.DefaultPosition, (170, 130), self.params_list, wx.LB_SINGLE)
        self.param_listbox.SetSelection(0)

        user_listbox_sizer.Add(self.user_listbox, 1,wx.ALL | wx.EXPAND, border = 10)
        user_listbox_sizer.Add(self.all_user_cb,0, wx.BOTTOM | wx.CENTER)
        process_listbox_sizer.Add(self.process_listbox, 1, wx.ALL | wx.EXPAND, border = 10)
        process_listbox_sizer.Add(self.all_process_cb,0, wx.BOTTOM | wx.CENTER)
        param_listbox_sizer.Add(self.param_listbox, 1, wx.ALL | wx.EXPAND, border = 10)

        gs.Add(user_listbox_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        gs.Add(process_listbox_sizer, 1,wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        gs.Add(param_listbox_sizer, 1,wx.ALL | wx.EXPAND | wx.ALIGN_TOP)

        panel.SetSizerAndFit(gs)

class FitApp(wx.App):
    def OnInit(self):
        frame = FitTopFrame(None, -1, 'listbox.py')
        frame.Centre()
        frame.Show(True)
        return True

fit_app = FitApp(0)
fit_app.MainLoop()
