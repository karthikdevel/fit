import pandas as pd
import numpy as np
import os
import wx
import threading
import time

def processMG(arg1):
    if arg1 == None:
        return float(0)
    elif 'm' in arg1:
        return float(arg1[:-1])*1048576
    elif 'g' in arg1:
        return float(arg1[:-1])*1048576*1024
    else:
        return float(arg1)

class TopDirParser:
    def __init__(self, start, end, targetdir=None):
        self.targetdir = targetdir
        self.filelist = os.listdir(self.targetdir)
        self.start_ts = start
        self.end_ts = end
        
    def LoadData(self, dlg, queue, numfiles):
        self.panel_dict = dict()
        files_loaded = 0
        start_time = time.time()
        for ifile in self.filelist:
            fs = pd.to_datetime(ifile[:ifile.find('.')])
            if fs >= pd.to_datetime(self.start_ts) and fs <= pd.to_datetime(self.end_ts):
                self.panel_dict[fs] = pd.read_csv(self.targetdir+ifile,
                                                  sep='\s+',
                                                  skiprows=range(6),
                                                  comment='<defunct>',
                                                  #usecols = ['RES'],
                                                  squeeze=False,
                                                  converters={'RES':processMG})
                
                files_loaded += 1
                process_rate = (time.time() - start_time)/files_loaded
                message = "Loaded :{0:^6}".format(files_loaded)+" of "+`numfiles`+" files at {0:.1f}".format(round(1/process_rate,2))+" Files/Sec "
                if dlg:
                    wx.CallAfter(dlg.Update,files_loaded,message)
                    if dlg.WasCancelled() == True:
                        dlg.EndModal(-1)
                        break
        if queue:
            queue.put(files_loaded)
        return True

    def GetItemList(self,item='USER'):
        if not self.panel_dict:
            return None
        else:
            x = set()
            for i in self.panel_dict:
                x |= set(self.panel_dict[i][item].unique())

            # Is this clean?
            # what else to remove?
            x.remove(None)
            return list(x)

    def GenDF(self, group, global_data = True,selector=dict()):
        DF = pd.DataFrame()
        panel_dict_user = dict()
        global_data_dict = dict()
        for fs in self.panel_dict:
            df = self.panel_dict[fs][['RES','%CPU','USER','COMMAND']]
            if global_data == True:
                global_data_dict[fs] = df['RES'].sum()

            for i in selector:
                df = df[df[i].map(lambda x: True if x in selector[i] else False)]
                df = df.reset_index(1,drop=True).drop(i,axis=1)
            panel_dict_user[fs] = df.groupby(group).sum().stack()

        DF = pd.concat(panel_dict_user,axis=1)
        DF.index.set_names(['major','minor'], inplace=True)

        if global_data == True:
            return DF,pd.Series(global_data_dict)
        else:
            return DF
