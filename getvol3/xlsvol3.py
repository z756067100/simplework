# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 09:08:36 2018

@author: hasee
"""

import xlwings as xw
import time
from WindPy import w
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from matplotlib.pylab import date2num
import datetime as dt
w.start()
import math


def calc_hist_vol(input_df, windows):
    df = input_df.copy()
    df["daily_return"] = df["CLOSE"].pct_change()
    df['square'] = df['daily_return'] ** 2  

    for i in range(len(windows)):
        df['vol_'+str(windows[i])] = df['square'].rolling(windows[i]).mean() * 244
        df['vol_'+str(windows[i])] = df['vol_'+str(windows[i])].apply(np.sqrt)
        # df = df.dropna()

    df = df.sort_index(ascending=False)
    return df.drop(['square'], 1)

def calc_parkinson_vol(input_df, windows):
    df = input_df.copy()
    df['log_h_l'] = np.log(df["HIGH"] / df["LOW"])
    
    df['square'] = df['log_h_l'] * df['log_h_l']
    for i in range(len(windows)):
        df['vol_'+str(windows[i])] = df['square'].rolling(windows[i]).mean() * 244 / math.log(2) / 4
        df['vol_'+str(windows[i])] = df['vol_'+str(windows[i])].apply(np.sqrt)
    df = df.sort_index(ascending=False)
    return df.drop(['square'], 1)

def calc_gk_vol(input_df, windows):
    df = input_df.copy()
    df_prev = df.shift(1)
    df['log_h_l'] = np.log(df["HIGH"] / df["LOW"])
    df['log_c_c'] = np.log(df["CLOSE"] / df_prev["CLOSE"])
    df['gk'] = (df['log_h_l']) **2 * 0.5 - 0.39 * (df['log_c_c']**2) * 0.39
    for i in range(len(windows)):
        df['vol_'+str(windows[i])] = df['gk'].rolling(windows[i]).mean() * 244
        df['vol_'+str(windows[i])] = df['vol_'+str(windows[i])].apply(np.sqrt)
    df = df.sort_index(ascending=False)
    return df.drop(['gk'], 1)

def drawvol():
    wb=xw.Book.caller()
    wb=xw.books.active
#    print wb
#    windows=[5,15,30,50]
    sht=wb.sheets['Sheet1']
#    sht_data=wb.sheets['data']
    code=sht.range('B1').value
    start=time.strftime('%Y-%m-%d',time.strptime(str(sht.range('B2').value),'%Y-%m-%d %H:%M:%S'))
    end=time.strftime('%Y-%m-%d',time.strptime(str(sht.range('B3').value),'%Y-%m-%d %H:%M:%S'))
    windows=[]
    for i in xrange(4,7):
        windows.append(int(sht.range('B%s' %i).value))
    
    st=dt.datetime.strptime(start,"%Y-%m-%d")-dt.timedelta(days=80)
    
    start_time=dt.datetime.strftime(st,"%Y-%m-%d")

    wsd_data=w.wsd(code, "close,high,low", start_time, end, "")
    input_df=pd.DataFrame(wsd_data.Data,index=['CLOSE','HIGH','LOW'])
    input_df=input_df.T
    result1=calc_hist_vol(input_df, windows)
    result2=calc_parkinson_vol(input_df, windows)
    result3=calc_gk_vol(input_df, windows)
    day=wsd_data.Times
#    day=pd.DataFrame(day)
    N=len(result2.iloc[:,4][~np.isnan(result2.iloc[:,4])])
#    result1=result1.sort_index()
#    result2=result2.sort_index()
#    result3=result3.sort_index()
#    result=pd.concat([day,result1.iloc[:,4],result2.iloc[:,4],result3.iloc[:,5]],axis=1)
#    result=result.dropna(axis=0,how='any')
#    
#    sht_data.range('A2:D2').expand().clear_contents()
#    sht_data.range('A2').options(index=False, header=False).value=result
    
    
    name1=np.random.normal()
    fig=plt.figure(str(name1),figsize=(6,4))      
    plt.plot(result1.iloc[:,4],label=str(windows[0]))
    plt.plot(result1.iloc[:,5],label=str(windows[1]))
    plt.plot(result1.iloc[:,6],label=str(windows[2]))
    def format_date(x, pos=None):
        thisind=np.clip(int(x+0.5), 0, N-1)
        return day[thisind]
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_date)) 
    plt.grid()
    plt.gca().set_title('hist_vol  '+str(code))
    plt.legend()
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(rotation=45)
    sht.pictures.add(fig, name=str(name1), update=False,left=sht.range('B30').left, top=sht.range('B7').top)

#   
    name2=np.random.normal()       
    fig3=plt.figure(str(name2),figsize=(6,4))      
    plt.plot(result3.iloc[:,5],label=str(windows[0]))
    plt.plot(result3.iloc[:,6],label=str(windows[1]))   
    plt.plot(result3.iloc[:,7],label=str(windows[2]))
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_date))   
    plt.grid()
    plt.gca().set_title('gk_vol  '+str(code))
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend() 
    plt.xticks(rotation=45)
    sht.pictures.add(fig3, name=str(name2), update=False,left=sht.range('Q30').left, top=sht.range('B7').top)

#    
    name3=np.random.normal()
    fig4=plt.figure(str(name3),figsize=(6,4))
    plt.plot(result2.iloc[:,4],label=str(windows[0]))
    plt.plot(result2.iloc[:,5],label=str(windows[1]))
    plt.plot(result2.iloc[:,6],label=str(windows[2]))
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
    plt.grid()
    plt.gca().set_title('parkinson'+str(code))
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend()
    plt.xticks(rotation=45)
    sht.pictures.add(fig4,name=str(name3),update=False,left=sht.range('I30').left,top=sht.range('B7').top)
    

    
    
  

#def getvolpictures()
#    wb=xw.Book.caller()
##wb=xw.books.active
##print wb
#    sht=wb.sheets['Sheet1']
#    code=sht.range('B1').value
#    start_time=time.strftime('%Y-%m-%d',time.strptime(str(sht.range('B2').value),'%Y-%m-%d %H:%M:%S'))
#    end_time=time.strftime('%Y-%m-%d',time.strptime(str(sht.range('B3').value),'%Y-%m-%d %H:%M:%S'))
#    cycle=sht.range('B4').value
#    getvol3.drawvol(code,start_time,end_time,cycle)
