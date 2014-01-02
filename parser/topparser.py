import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
import random

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
    def __init__(self,targetdir=None,analyze='USER'):
        
        if targetdir != None:
            filelist = os.listdir(targetdir) 
            
            self.panel_dict = dict()
            for ifile in filelist:
                fs = pd.to_datetime(ifile[:ifile.find('.')])
                self.panel_dict[fs] = pd.read_csv(targetdir+ifile,
                                                        sep='\s+',
                                                        skiprows=range(6),
                                                        comment='<defunct>',
                                                        #usecols = ['RES'],
                                                        squeeze=False,
                                                        converters={'RES':processMG})
    def GetUserList(self):
        if not self.panel_dict:
            return None
        else:
            x = set()
            for i in self.panel_dict:
                x |= set(self.panel_dict[i]['USER'].unique())
             
            #is this clean?   
            x.remove(None)
            return list(x)
    
    def GetProcessList(self):
        if not self.panel_dict:
            return None
        else:
            x = set()
            for i in self.panel_dict:
                x |= set(self.panel_dict[i]['COMMAND'].unique())
            
            #is this clean? 
            x.remove(None)
            return list(x)

    def GenDFUser(self, process_sel_list):
        DF_user = pd.DataFrame()
        panel_dict_user = dict()
        for fs in self.panel_dict:
            df = self.panel_dict[fs][['RES','%CPU','USER','COMMAND']]
            df = df[df['COMMAND'].map(lambda x: True if x in process_sel_list else False)]
            DF_user = df.reset_index(1,drop=True).drop('COMMAND',axis=1)
            panel_dict_user[fs] = DF_user.groupby('USER').sum()
        
        pnl = pd.Panel.from_dict(panel_dict_user)
        DF_user = pnl.to_frame(filter_observations=False)        
        return DF_user
    
    def GenDFProcess(self,user_sel_list):
        DF_process = pd.DataFrame()
        panel_dict_process = dict()
        for fs in self.panel_dict:
            df = self.panel_dict[fs][['RES','%CPU','USER','COMMAND']]
            df = df[df['USER'].map(lambda x: True if x in user_sel_list else False)]
            DF_process = df.reset_index(1,drop=True).drop('USER',axis=1)
            panel_dict_process[fs] = DF_process.groupby('COMMAND').sum()
        
        pnl = pd.Panel.from_dict(panel_dict_process)
        DF_process = pnl.to_frame(filter_observations=False)        
        return DF_process    
