# -*- coding: utf-8 -*-
"""
Created on Wed May 02 12:22:19 2018

@author: hasee
"""

from WindPy import w
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib as mpl
import matplotlib.finance as mpf 
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.pylab import date2num
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
import datetime as dt

import xlwings as xw
w.start()
def draw():
    wb=xw.books.active
    wb=xw.Book.caller()
    sht=wb.sheets[0]
    start=str(sht.range('B1').value)
    end=str(sht.range('B2').value)
    r=0.048
    wsi_data=w.wsi("510050.SH", "close", start, end, "BarSize=5;periodstart=09:00:00;periodend=15:30:51")
    ETFprice=pd.Series(wsi_data.Data[0],index=pd.to_datetime(wsi_data.Times))
    ETFprice1=ETFprice.to_period('D')
    index=[]
    for i in range(len(ETFprice)-1):
        if ETFprice1.index[i]!=ETFprice1.index[i+1]:
            index.append(i)
    index.append(-1)
    
    ETFclose=[]       
    ETFclose=ETFprice1[index]
    result=pd.DataFrame()
    
    for i in xrange(1,len(ETFclose),1):
        T=str(ETFclose.index[i])
        optioncode=w.wset("optionchain",
                           u'date=%s;us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put,expiredate' %(T))
        optioninfo=pd.DataFrame(optioncode.Data)
        optioninfo=optioninfo.T
        optioninfo00=optioninfo[optioninfo.iloc[:,2]==optioninfo.iloc[0,2]]  
        ups=np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])
        
        optioninfo00ATM=optioninfo00[np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])==ups.min()]# 最小值的行即ATM的行
    
        st=datetime.strptime(str(ETFclose.index[i]),"%Y-%m-%d")
        start_time=datetime.strftime(st,"%Y-%m-%d %H:%M:%S")
#        et=time.strptime(str(ETFclose.index[i+1]),"%Y-%m-%d")
#        end_time=time.strftime("%Y-%m-%d %H:%M:%S",et)
        et=st+dt.timedelta(days=1)
        end_time=datetime.strftime(et,"%Y-%m-%d %H:%M:%S")
        #ATM，近期合约
        ATMC00data=w.wsi(optioninfo00ATM.iloc[0,0], "close", start_time, end_time, "BarSize=5")
        ATMP00data=w.wsi(optioninfo00ATM.iloc[1,0], "close", start_time, end_time, "BarSize=5")
        ATMC00price=pd.DataFrame(ATMC00data.Data)
        ATMP00price=pd.DataFrame(ATMP00data.Data)
        ATMC00price=ATMC00price.T
        ATMP00price=ATMP00price.T
        t1=optioninfo00ATM.iloc[0,4]/float(365)
    #    dayleft=pd.DataFrame(ATMC00data.Data[0])
    #    dayleft.iloc[:,0]=4
        if ATMC00price.iloc[0,0]!='No Content':  
            FATM00=(ATMC00price.iloc[:,0]-ATMP00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATM.iloc[0,1]
            ResultATM00=pd.DataFrame(FATM00)
            ResultATM00.index=pd.to_datetime(ATMC00data.Times)
            ResultATM00.columns=['priceATM00']
        else:
            ResultATM00=pd.DataFrame(index=ATMC00data.Times,columns=['priceATM00'])
        ResultATM00['dayleft']=optioninfo00.iloc[0,4]
    
        Result1day=pd.concat([ResultATM00],axis=1)
        result=pd.concat([result,Result1day],axis=0)
        
    result['ETFprice']=ETFprice    
    

    
    ##减去ETF现价
    result.iloc[:,0]=result.iloc[:,0]-result.iloc[:,2]
    result.iloc[:,1]=result.iloc[:,1]/365*r*result.iloc[:,2]
    
    ## 减去资金成本
    result.iloc[:,0]=result.iloc[:,0]-result.iloc[:,1]     
    
    ##将其分为假期间隔后和间隔前
    result1=result.reset_index()
    result2=result1.shift(48)
    firstday=result[[x.days>1 for x in (result1.iloc[:,0]-result2.iloc[:,0])]]
    continueday=result[[x.days==1 for x in (result1.iloc[:,0]-result2.iloc[:,0])]]
    
    firstday=pd.DataFrame(firstday.iloc[:,0].describe()).T  
    continueday=pd.DataFrame(continueday.iloc[:,0].describe()).T    
    
    firstday=pd.concat([firstday.loc[:,'25%'],firstday.loc[:,'min'],firstday.loc[:,'max'],firstday.loc[:,'75%']],axis=1)
    continueday=pd.concat([continueday.loc[:,'25%'],continueday.loc[:,'min'],continueday.loc[:,'max'],continueday.loc[:,'75%']],axis=1)
 #####各数据已经做好，只差画蜡烛图   
    candle=pd.concat([firstday,continueday],axis=0)
    stock_array=np.append(np.arange(2).reshape(2,1),candle.values,axis=1)
    
    name=np.random.normal()
    fig=plt.figure(str(name),figsize=(8,4))
    ax1=plt.subplot(111)
    candlestick_ohlc(ax1, stock_array, colorup = "red", colordown="green")
    plt.grid()
    ax1.set_title("Weekday spreads")
    plot1=sht.pictures.add(fig, name=str(name), update=False,left=sht.range('C30').left, top=sht.range('B7').top)
       

  

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    
#    
#    
#    
#    
#    
#    ##将数据分为每日
#    Monday=result[[x.isoweekday()==1 for x in result.index]]
#    Tuesday=result[[x.isoweekday()==2 for x in result.index]]
#    Wednesday=result[[x.isoweekday()==3 for x in result.index]]
#    Thursday=result[[x.isoweekday()==4 for x in result.index]]
#    Friday=result[[x.isoweekday()==5 for x in result.index]]
#    
#    
#    
#    #找到画K线图的各个统计指标
#    Monday_desc=pd.DataFrame(Monday['priceATM00'].describe()).T
#    candle1=pd.concat([Monday_desc['25%'],Monday_desc['max'],Monday_desc['min'],Monday_desc['75%']],axis=1)
#    Tuesday_desc=pd.DataFrame(Tuesday['priceATM00'].describe()).T
#    candle2=pd.concat([Tuesday_desc['25%'],Tuesday_desc['max'],Tuesday_desc['min'],Tuesday_desc['75%']],axis=1)
#    Wednesday_desc=pd.DataFrame(Wednesday['priceATM00'].describe()).T
#    candle3=pd.concat([Wednesday_desc['25%'],Wednesday_desc['max'],Wednesday_desc['min'],Wednesday_desc['75%']],axis=1)
#    Thursday_desc=pd.DataFrame(Thursday['priceATM00'].describe()).T
#    candle4=pd.concat([Thursday_desc['25%'],Thursday_desc['max'],Thursday_desc['min'],Thursday_desc['75%']],axis=1)
#    Friday_desc=pd.DataFrame(Friday['priceATM00'].describe()).T
#    candle5=pd.concat([Friday_desc['25%'],Friday_desc['max'],Friday_desc['min'],Friday_desc['75%']],axis=1)
#    candle=pd.concat([candle1,candle2,candle3,candle4,candle5],axis=0)
#    candle.reset_index(inplace=True)
#    candle.drop(candle.columns[0],axis=1,inplace=True)
#    candle=candle*1000
#    
#    average=pd.DataFrame(pd.concat([Monday_desc['mean'],Tuesday_desc['mean'],Wednesday_desc['mean'],Thursday_desc['mean'],Friday_desc['mean']],axis=0))
#    average.reset_index(inplace=True)
#    average.drop(average.columns[0],axis=1,inplace=True)    
#    average=average*1000
#    fig=plt.figure('fig1',figsize=(20,20)) 
#    ax1=plt.subplot(111)
#    candle=pd.concat([pd.DataFrame(np.arange(5),index=np.arange(5)),average,average,average,average],axis=1)
#    stock_array=np.array(candle)
#    ax1.plot(average)
#    candlestick_ohlc(ax1, stock_array, colorup = "red", colordown="green", width=0.2)
#    plt.xticks([0,1,2,3,4],['Monday','Tuesday','Wednesday','Thursday','Friday'])
#    #mpf.plot_day_summary_oclh(ax1, stock_array, colorup = "red", colordown="green")
#    ax1.set_title("Weekday spreads")
#    plot1=sht.pictures.add(fig, name='fig', update=False,left=sht.range('C30').left, top=sht.range('B7').top)
#    plot1.height/=2.3
#    plot1.width/=2.0
