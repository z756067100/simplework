# -*- coding: utf-8 -*-
"""
Created on Thu May 03 13:59:24 2018

@author: hasee
"""

from WindPy import w
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import matplotlib as mpl
import matplotlib.finance as mpf 
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.pylab import date2num
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
w.start()
dealdata=pd.DataFrame.from_csv('E:/judge.csv')
w_wsi=w.wsi("510050.SH", "close", "2017-09-01 09:00:00", "2018-05-03 14:04:16", "BarSize=5;PriceAdj=F")
ETF50=pd.Series(w_wsi.Data[0],index=w_wsi.Times)
w_wsi=w.wsi("000016.SH", "close", "2017-09-01 09:00:00", "2018-05-03 14:04:16", "BarSize=5;PriceAdj=F")
index50=pd.Series(w_wsi.Data[0],index=w_wsi.Times)
w_wsi=w.wsi("IH.CFE", "close", "2017-09-01 09:00:00", "2018-05-03 14:04:16", "BarSize=5;PriceAdj=F")
IH=pd.Series(w_wsi.Data[0],index=w_wsi.Times)
names = locals()
for i in range(len(dealdata.columns)):
    start=str(dealdata[dealdata.iloc[:,i]].iloc[:,i].index[0])
    end=str(dealdata[dealdata.iloc[:,i]].iloc[:,i].index[-1]+dt.timedelta(days=1))
    code=dealdata.columns[i]
    w_wsi=w.wsi(code, "close", start, end, "BarSize=5;PriceAdj=F")
    names['%s' %code[:6]]=pd.Series(w_wsi.Data[0],index=w_wsi.Times)-index50
    
#r1=IH1709-ETF50
#s1=IH1709-index50
#为画excel所用的数据
dealdata=pd.concat([ETF50,index50,IH],axis=1)
dealdata=dealdata[~np.isnan(dealdata.iloc[:,0])]
dealdata.to_csv("ETF,index,IH.csv",index=True)


result=pd.concat([ETF50,index50,IH1709,IH1710,IH1711,IH1712,IH1801,IH1802,IH1803,IH1804,IH1805],axis=1) 
resultindex=pd.concat([ETF50,index50,IH1709,IH1710,IH1711,IH1712,IH1801,IH1802,IH1803,IH1804,IH1805],axis=1)
result=result[~np.isnan(result.iloc[:,0])]
result.reset_index(inplace=True)
resultindex=resultindex[~np.isnan(resultindex.iloc[:,0])]
resultindex.reset_index(inplace=True)


N=len(result)
ax=plt.subplot(111)
ax.plot(result.iloc[:,[3,4,5,6,7,8,9,10,11]])
ax.plot(resultindex.iloc[:,[3,4,5,6,7,8,9,10,11]],'--')
ax.plot(result.iloc[:,2]-result.iloc[:,1]*1000,'--')
#ax.hist(result.iloc[:,[3,4,5,6,7,8,9,10,11]]+result.iloc[:,1]*1000-result.iloc[:,2],bins=200,alpha=0.5)
def format_date(x, pos=None):
    thisind=np.clip(int(x+0.5), 0, N-1)
    return result.iloc[:,0][thisind]
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_date)) 
ax2=ax.twinx()
ax2.plot(result.iloc[:,1])


