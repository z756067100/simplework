# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:11:28 2018

@author: hasee
"""

from WindPy import w
import numpy as np
import pandas as pd
import datetime as dt
import time
import matplotlib as mpl
import matplotlib.finance as mpf 
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.pylab import date2num
from matplotlib import dates as mdates
from matplotlib import ticker as mticker

r=0.048



w.start()
wsi_data=w.wsi("510050.SH", "close", "2017-8-11 09:00:00", "2018-04-31 23:32:00", "BarSize=5;periodstart=09:00:00;periodend=15:30:51")
ETFprice=pd.Series(wsi_data.Data[0],index=pd.to_datetime(wsi_data.Times))
ETFprice.index[0]
ETFprice1=ETFprice.to_period('D')
wsi_datagc001=w.wsi("204001.SH", "close", "2017-8-11 09:00:00", "2018-04-31 23:31:23", "BarSize=5")
GC001price=pd.Series(wsi_data.Data[0],index=wsi_data.Times)
index=[]
for i in range(len(ETFprice)-1):
    if ETFprice1.index[i]!=ETFprice1.index[i+1]:
        index.append(i)

ETFclose=[]       
ETFclose=ETFprice1[index]
result1=pd.DataFrame()
result2=pd.DataFrame()


for i in xrange(1,len(ETFclose)-1,1):
    T=str(ETFclose.index[i])
    optioncode=w.wset("optionchain",
                       u'date=%s;us_code=510050.SH;option_var=全部;call_put=全部;field=option_code,strike_price,month,call_put,expiredate' %(T))
    optioninfo=pd.DataFrame(optioncode.Data)
    optioninfo=optioninfo.T
    position=[]
    
    for j in range(len(optioninfo)-1):
        if optioninfo.iloc[j,2]!=optioninfo.iloc[j+1,2]:
            position.append(j)
            
    optioninfo00=optioninfo[optioninfo.iloc[:,2]==201803]
    optioninfo01=optioninfo[optioninfo.iloc[:,2]==201803]
    
    if optioninfo00.shape[0]!=0:    
        optioninfo00=optioninfo00[optioninfo00.iloc[:,1]*100%5==0]
        ups=np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])   
        optioninfo00ATM=optioninfo00[np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])==ups.min()]#
        if optioninfo00ATM.shape!=(2,5):
            optioninfo00ATM=optioninfo00ATM.iloc[[0,2],:]  
        st=time.strptime(str(ETFclose.index[i]),"%Y-%m-%d")
        start_time=time.strftime("%Y-%m-%d %H:%M:%S",st)
        et=time.strptime(str(ETFclose.index[i+1]),"%Y-%m-%d")
        end_time=time.strftime("%Y-%m-%d %H:%M:%S",et)
        ATMC00data=w.wsi(optioninfo00ATM.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
        ATMP00data=w.wsi(optioninfo00ATM.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
        ATMC00price=pd.DataFrame(ATMC00data.Data)
        ATMP00price=pd.DataFrame(ATMP00data.Data)
        ATMC00price=ATMC00price.T
        ATMP00price=ATMP00price.T
        t1=optioninfo00ATM.iloc[0,4]/float(365)
        if ATMC00price.iloc[0,0]!='No Content':  
            FATM00=(ATMC00price.iloc[:,0]-ATMP00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATM.iloc[0,1]
            ResultATM00=pd.concat([FATM00,ATMC00price.iloc[:,1],ATMP00price.iloc[:,1]],axis=1)
            ResultATM00.index=ATMC00data.Times
            ResultATM00.columns=['priceATM00','callvolumeATM00','putvolumeATM00']
        else:
            ResultATM00=pd.DataFrame(index=ATMC00data.Times,columns=['priceATM00','callvolumeATM00','putvolumeATM00'])
        ResultATM00['dayleft']=optioninfo00.iloc[0,4]
#    dayleft=pd.DataFrame(ATMC00data.Data[0])
#    dayleft.iloc[:,0]=4
        if ATMC00price.iloc[0,0]!='No Content':  
            FATM00=(ATMC00price.iloc[:,0]-ATMP00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATM.iloc[0,1]
            ResultATM00=pd.concat([FATM00,ATMC00price.iloc[:,1],ATMP00price.iloc[:,1]],axis=1)
            ResultATM00.index=ATMC00data.Times
            ResultATM00.columns=['priceATM00','callvolumeATM00','putvolumeATM00']
        else:
            ResultATM00=pd.DataFrame(index=ATMC00data.Times,columns=['priceATM00','callvolumeATM00','putvolumeATM00'])
        ResultATM00['dayleft0']=optioninfo00.iloc[0,4]
        result1=pd.concat([result1,ResultATM00],axis=0)
    
    
    
    if optioninfo01.shape[0]!=0:
        optioninfo01=optioninfo01[optioninfo01.iloc[:,1]*100%5==0]
        ups=np.abs(optioninfo01.loc[:,1]-ETFclose[i-1])    
        optioninfo01ATM=optioninfo01[np.abs(optioninfo01.loc[:,1]-ETFclose[i-1])==ups.min()]  # 最小值的行即ATM的行
        if optioninfo01ATM.shape!=(2,5):
            optioninfo01ATM=optioninfo01ATM.iloc[[0,2],:] 
        
        st=time.strptime(str(ETFclose.index[i]),"%Y-%m-%d")
        start_time=time.strftime("%Y-%m-%d %H:%M:%S",st)
        et=time.strptime(str(ETFclose.index[i+1]),"%Y-%m-%d")
        end_time=time.strftime("%Y-%m-%d %H:%M:%S",et)
    

    
        ATMC01data=w.wsi(optioninfo01ATM.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
        ATMP01data=w.wsi(optioninfo01ATM.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
        ATMC01price=pd.DataFrame(ATMC01data.Data)
        ATMP01price=pd.DataFrame(ATMP01data.Data)
        ATMC01price=ATMC01price.T
        ATMP01price=ATMP01price.T
        t2=optioninfo01ATM.iloc[0,4]/float(365)
        
        if ATMC01price.iloc[0,0]!='No Content':      
            FATM01=(ATMC01price.iloc[:,0]-ATMP01price.iloc[:,0])*np.exp(0.05*t2)+optioninfo01ATM.iloc[0,1]
            ResultATM01=pd.concat([FATM01,ATMC01price.iloc[:,1],ATMP01price.iloc[:,1]],axis=1)
            ResultATM01.index=ATMC01data.Times
            ResultATM01.columns=['priceATM01','callvolumeATM01','putvolumeATM01'] 
        else:
            ResultATM01=pd.DataFrame(index=ATMC00data.Times,columns=['priceATM01','callvolumeATM01','putvolumeATM01'])
        ResultATM01['dayleft1']=optioninfo01.iloc[0,4]
        result2=pd.concat([result2,ResultATM01],axis=0)
result=pd.concat([result1,result2],axis=1)
result['ETFprice']=ETFprice
ETFclose=np.log(ETFprice)
ETFreturn=ETFclose.diff(1)
ETFvol=pd.Series(index=ETFreturn.index)
for i in range(len(ETFvol)):
    if i>=20:
        ETFvol[i]=np.std(ETFreturn[i-20:i])
    else:
        ETFvol[i]=0
dealdata=result    

dealdata.iloc[:,0]=dealdata.iloc[:,0]-dealdata.iloc[:,8]
dealdata.iloc[:,4]=dealdata.iloc[:,4]-dealdata.iloc[:,8]  

dealdata.iloc[:,3]=dealdata.iloc[:,3]/365*r*dealdata.iloc[:,8]

dealdata.iloc[:,7]=dealdata.iloc[:,7]/365*r*dealdata.iloc[:,8]  

dealdata['vol']=dealdata.iloc[:,8]
data=dealdata.to_period('D')
for j in xrange(0,len(ETFvol)):
    dealdata['vol'][data.index==ETFvol.index[j]]=ETFvol[j]
dealdata['GC001']=GC001price
dealdata=dealdata.dropna(axis=0,how='any')

plt.figure()
ax1=plt.subplot(211)
N=len(dealdata.iloc[:,0])
ind=np.arange(len(dealdata.iloc[:,0]))
#ax1.plot(ind,dealdata.iloc[:,0]-dealdata.iloc[:,3],label='ATM00')#减去资金成本
ax1.plot(ind,dealdata.iloc[:,0]*1000,label='March')#不减去资金成本
ax1.plot(ind,dealdata.iloc[:,3]*1000)
def format_date(x, pos=None):
    thisind=np.clip(int(x+0.5), 0, N-1)
    #thisind=int(np.round(x))#保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
    return dealdata.index[thisind]
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
#fig.autofmt_xdate() 
plt.legend()
ax1.grid()
ax1.set_title('March Option')
ax3=ax1.twinx()
ax3.plot(ind,dealdata['GC001'],'red',label='GC001')

ax2=plt.subplot(212)
#ax2.plot(ind,dealdata.iloc[:,4]*1000,label='March')
#ax2.plot(ind,dealdata.iloc[:,7]*1000)
ax2.plot(ind,dealdata.iloc[:,8])
ax2.grid()
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
plt.legend()
ax2.set_title('price and vol')
ax3=ax2.twinx()
ax3.plot(ind,np.sqrt(244)*dealdata.iloc[:,9])
#ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
#ax1.set_title("ATM00 ETFprice")
#ax2.grid()
        
        
        
        