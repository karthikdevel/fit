import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
import random

randn = np.random.randn

myglobal = np.arange(100)
myglobalidx = 1

def processMG(arg1):
    #return myglobal[myglobalidx%100]
    #return float(myglobalidx%100)
    if arg1 == None:
        return float(0)
    elif 'm' in arg1:
        return float(arg1[:-1])*1048576
    elif 'g' in arg1:
        return float(arg1[:-1])*1048576*1024
    else:
        return float(arg1)

        
#def gen_user_time_series(panel, user, resource):
    
def top_dir_parser(targetdir ='/home/karthik/work/python/bigdata/topreports/'):
    filelist = os.listdir(targetdir) 
    
    panel_dict=dict()
    
    for ifile in filelist:
        ifilestamp=pd.to_datetime(ifile[:ifile.find('.')])
        panel_dict[ifilestamp] = pd.read_csv(targetdir+ifile,
                                                sep='\s+',
                                                skiprows=range(6),
                                                comment='<defunct>')
    
        panel_dict[ifilestamp]['RES'] = panel_dict[ifilestamp]['RES'].map(processMG)
        myglobalidx += 1
        #tempgrouped = panel_dict[ifilestamp]['RES'].groupby(panel_dict[ifilestamp]['USER'])
    
    pnl=pd.Panel.from_dict(panel_dict)
    
    return pnl
    
    #plt.plot(pnl.keys(),[pnl[i]['RES'].max() for i in pnl.keys()])
    #total_data = pd.DataFrame()
    #total_data = pd.concat(panel_dict.values())
    
    #total_data = total_data.fillna('0')
    #total_data['RES'] = total_data['RES'].map(processMG)
    #grouped = total_data['RES'].groupby(total_data['USER'])
    
    #fig, axes = plt.subplots(2, 2)
    #temp = grouped.mean().plot(kind='bar',ax=axes[0,0],title='mean')
    #grouped.std().plot(kind='bar',ax=axes[1,0],title='std')
    #temp=grouped.min().plot(kind='bar',ax=axes[0,1],title='min',ylim=temp.get_ylim())
    #grouped.max().plot(kind='bar',ax=axes[1,1],title='max')
    
    
