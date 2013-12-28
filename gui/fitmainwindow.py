import wx

class FitMainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (350, 150))

        self.SetMinSize((350, 150))

        self.panel = wx.Panel(self, -1)

        # top level sizer.
        self.main_grid_bag_sizer = wx.GridBagSizer(9,9)
        
        self.dir_name = wx.TextCtrl(self.panel, wx.ID_ANY, size=(180, 20))
        self.log_path = wx.Button(self.panel, wx.ID_ANY, "Logs Path")
        self.log_path.Bind(wx.EVT_BUTTON, self.opendir)
        
        # Check grid_bag to select Top/Free/IOStat
        self.top_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Top')
        self.top_cb.SetValue(False)
        self.free_cb = wx.CheckBox(self.panel, wx.ID_ANY, 'Free')
        self.free_cb.SetValue(False)

        self.launch_button = wx.Button(self.panel, wx.ID_ANY, "Launch")

        # Add to the correct grid_bag.
        self.main_grid_bag_sizer.Add(self.dir_name, (0,0), (1,3), flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.log_path, (0,3), wx.DefaultSpan, flag =  wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.top_cb, (1,0), wx.DefaultSpan, flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.free_cb, (1,1), wx.DefaultSpan, flag = wx.EXPAND)
        self.main_grid_bag_sizer.Add(self.launch_button, (2,2), wx.DefaultSpan, flag = wx.EXPAND)
        
        for i in range(3):
            self.main_grid_bag_sizer.AddGrowableRow(i,1)
        for i in range(4):
            self.main_grid_bag_sizer.AddGrowableCol(i,1)

        self.panel.SetSizerAndFit(self.main_grid_bag_sizer)
    
    def opendir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_name.SetValue(dlg.GetPath())
        dlg.Destroy()
        
    def get_current_dir(self):
        return self.dir_name.GetValue()
    
    def bind_launch_button(self, handler):
        self.launch_button.Bind(wx.EVT_BUTTON,handler)
        
