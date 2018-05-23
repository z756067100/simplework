# -*- coding: utf-8 -*-
"""
Created on Wed May 09 15:03:09 2018

@author: hasee
"""

from WindPy import w
import numpy as np
import pandas as pd
import datetime as dt
import xlwings as xw
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
from matplotlib import dates as mdates
from matplotlib import ticker as mticker

w.start()

def draw():
    wb=xw.Book.caller()
    wb=xw.books.active
    sht=wb.sheets[0]
    r=sht.range('C213').value
    end=sht.range('J2').value
    w_wsd=w.wsd("510050.SH", "close", "ED-20TD", end, "")
    ETFclose=pd.Series(w_wsd.Data[0],index=w_wsd.Times)
    resultcontango=pd.DataFrame() 
    for i in xrange(1,len(ETFclose),1):
        T=ETFclose.index[i]    
        optioncode=w.wset("optionchain",
                           u'date=%s;us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put,expiredate' %(T))
        optioninfo=pd.DataFrame(optioncode.Data)
        optioninfo=optioninfo.T
        optioninfo=optioninfo[optioninfo.iloc[:,1]*100%5==0]#去掉行权价格为零头的期权
        optioninfo.columns=['Code','K','ex_day','C or P','T_days']  
        optioninfo['trade day']=T
        optioninfo.reset_index(inplace=True)
        optioninfo.drop(optioninfo.columns[0],axis=1,inplace=True)   
        #找到ATM
        ups=np.abs(optioninfo.iloc[:,1]-ETFclose[i-1])
        optioninfo=optioninfo[ups==np.min(ups)]
    ##找到00
        optioninfo=optioninfo[optioninfo.iloc[:,2]==optioninfo.iloc[0,2]]  
    ##找到期权价格
        w_wsdoption=w.wsd(optioninfo['Code'].tolist(), "close", T, T, "")
        optioninfo['price']=w_wsdoption.Data[0]  
        optioninfo['ETFprice']=ETFclose[i]      
        F=(optioninfo.iloc[0,6]-optioninfo.iloc[1,6])*np.exp((-r*(optioninfo.iloc[0,4]+1))/365)+optioninfo.iloc[0,1]
        contangorate=pd.Series((F-optioninfo.iloc[0,7])/optioninfo.iloc[0,7]/(optioninfo.iloc[0,4]+1)*365)
        contangorate.index=[T]
        resultcontango=pd.concat([resultcontango,contangorate],axis=0)
