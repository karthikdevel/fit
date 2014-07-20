import wx

class FitListBox(wx.ListBox):
    def GetDropList(self, itemlist):
        selections = [self.GetString(i) for i in self.GetSelections()]
        drop_list = []
        for i in itemlist:
            if i not in selections:
                drop_list.append(i)

        return drop_list

    def GetSelList(self, itemlist):
        selections = [self.GetString(i) for i in self.GetSelections()]
        sel_list = []
        for i in itemlist:
            if i in selections:
                sel_list.append(i)

        return sel_list
