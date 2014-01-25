import pandas as pd
import numpy as np
import os

randn = np.random.randn

myglobal = np.arange(100)
myglobalidx = 1

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
        
        if targetdir != None:
            filelist = os.listdir(targetdir) 
            
            self.panel_dict = dict()
            for ifile in filelist:
                fs = pd.to_datetime(ifile[:ifile.find('.')])
                if fs >= pd.to_datetime(start) and fs <= pd.to_datetime(end):
                    self.panel_dict[fs] = pd.read_csv(targetdir+ifile,
                                                        sep='\s+',
                                                        skiprows=range(6),
                                                        comment='<defunct>',
                                                        #usecols = ['RES'],
                                                        squeeze=False,
                                                        converters={'RES':processMG})

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
            panel_dict_user[fs] = df.groupby(group).sum()
        
        pnl = pd.Panel.from_dict(panel_dict_user)
        DF = pnl.to_frame(filter_observations=False)

        if global_data == True:
            return DF,pd.Series(global_data_dict)
        else:
            return DF

