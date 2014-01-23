import wx

class FitListBox(wx.ListBox):
    def GetDropList(self, itemlist):
        sel_list = [self.GetString(i) for i in self.GetSelections()]
        drop_list = []
        for i in itemlist:
            if i not in sel_list:
                drop_list.append(i)
                
        return drop_list
    
    def GetSelList(self, itemlist):
        sel_list = [self.GetString(i) for i in self.GetSelections()]
        drop_list = []
        for i in itemlist:
            if i in sel_list:
                drop_list.append(i)
                
        return drop_list      