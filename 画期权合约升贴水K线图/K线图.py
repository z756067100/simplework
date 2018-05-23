# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:46:16 2018

@author: hasee
"""
from WindPy import w
import numpy as np
import pandas as pd
from datetime import datetime
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
wsi_data=w.wsi("510050.SH", "close", "2018-01-01 09:00:00", "2018-04-28 23:32:00", "BarSize=5;periodstart=09:00:00;periodend=15:30:51")
ETFprice=pd.Series(wsi_data.Data[0],index=pd.to_datetime(wsi_data.Times))

ETFprice1=ETFprice.to_period('D')
index=[]
for i in range(len(ETFprice)-1):
    if ETFprice1.index[i]!=ETFprice1.index[i+1]:
        index.append(i)

ETFclose=[]       
ETFclose=ETFprice1[index]
result=pd.DataFrame()
#
#ETFclose.to_csv("ETFclose.csv",index=True)
#ETFprice.to_csv("ETFprice.csv",index=True)



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
            
    optioninfo00=optioninfo.iloc[0:position[0]+1,:]
    optioninfo01=optioninfo.iloc[position[0]+1:position[1]+1,:]

    
    ups=np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])
    
    optioninfo00ATM=optioninfo00[np.abs(optioninfo00.loc[:,1]-ETFclose[i-1])==ups.min()]# 最小值的行即ATM的行
    if optioninfo00ATM.shape!=(2,5):
        optioninfo00ATM=optioninfo00ATM.iloc[[0,2],:]        
    optioninfo00ATMN1=optioninfo00.loc[(optioninfo00ATM.index-1).tolist(),:]
    optioninfo00ATMP1=optioninfo00.loc[(optioninfo00ATM.index+1).tolist(),:]
    
    ups=np.abs(optioninfo01.loc[:,1]-ETFclose[i-1])
    
    optioninfo01ATM=optioninfo01[np.abs(optioninfo01.loc[:,1]-ETFclose[i-1])==ups.min()]  # 最小值的行即ATM的行
    if optioninfo01ATM.shape!=(2,5):
        optioninfo01ATM=optioninfo01ATM.iloc[[0,2],:] 
    optioninfo01ATMN1=optioninfo01.loc[(optioninfo01ATM.index-1).tolist(),:]
    optioninfo01ATMP1=optioninfo01.loc[(optioninfo01ATM.index+1).tolist(),:]
    

    st=time.strptime(str(ETFclose.index[i]),"%Y-%m-%d")
    start_time=time.strftime("%Y-%m-%d %H:%M:%S",st)
    et=time.strptime(str(ETFclose.index[i+1]),"%Y-%m-%d")
    end_time=time.strftime("%Y-%m-%d %H:%M:%S",et)
    
    #ATM，近期合约
    ATMC00data=w.wsi(optioninfo00ATM.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMP00data=w.wsi(optioninfo00ATM.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMC00price=pd.DataFrame(ATMC00data.Data)
    ATMP00price=pd.DataFrame(ATMP00data.Data)
    ATMC00price=ATMC00price.T
    ATMP00price=ATMP00price.T
    t1=optioninfo00ATM.iloc[0,4]/float(365)
#    dayleft=pd.DataFrame(ATMC00data.Data[0])
#    dayleft.iloc[:,0]=4
    if ATMC00price.iloc[0,0]!='No Content':  
        FATM00=(ATMC00price.iloc[:,0]-ATMP00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATM.iloc[0,1]
        ResultATM00=pd.concat([FATM00,ATMC00price.iloc[:,1],ATMP00price.iloc[:,1]],axis=1)
        ResultATM00.index=ATMC00data.Times
        ResultATM00.columns=['priceATM00','callvolumeATM00','putvolumeATM00']
    else:
        ResultATM00=pd.DataFrame(index=ATMC00data.Times,columns=['priceATM00','callvolumeATM00','putvolumeATM00'])
    ResultATM00['dayleft']=optioninfo00.iloc[0,4]

    
    #ATM，下期合约
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
    ResultATM01['dayleft']=optioninfo01.iloc[0,4]
    
    #ATM-1,近期合约
    ATMN1C00data=w.wsi(optioninfo00ATMN1.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMN1P00data=w.wsi(optioninfo00ATMN1.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMN1C00price=pd.DataFrame(ATMN1C00data.Data)
    ATMN1P00price=pd.DataFrame(ATMN1P00data.Data)
    ATMN1C00price=ATMN1C00price.T
    ATMN1P00price=ATMN1P00price.T
    if ATMN1C00price.iloc[0,0]!='No Content':  
        FATMN100=(ATMN1C00price.iloc[:,0]-ATMN1P00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATMN1.iloc[0,1]
        ResultATMN100=pd.concat([FATMN100,ATMN1C00price.iloc[:,1],ATMN1P00price.iloc[:,1]],axis=1)    
        ResultATMN100.index=ATMN1C00data.Times    
        ResultATMN100.columns=['priceATMN100','callvolumeATMN100','putvolumeATMN100']  
    else:
        ResultATMN100=pd.DataFrame(index=ATMC00data.Times,columns=['priceATMN100','callvolumeATMN100','putvolumeATMN100'])
    ResultATMN100['dayleft']=optioninfo00.iloc[0,4]

    #ATM-1,下期合约
    ATMN1C01data=w.wsi(optioninfo01ATMN1.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMN1P01data=w.wsi(optioninfo01ATMN1.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMN1C01price=pd.DataFrame(ATMN1C01data.Data)
    ATMN1P01price=pd.DataFrame(ATMN1P01data.Data)
    ATMN1C01price=ATMN1C01price.T
    ATMN1P01price=ATMN1P01price.T
    if ATMN1C01price.iloc[0,0]!='No Content': 
        FATMN101=(ATMN1C01price.iloc[:,0]-ATMN1P01price.iloc[:,0])*np.exp(0.05*t2)+optioninfo01ATMN1.iloc[0,1]
        ResultATMN101=pd.concat([FATMN101,ATMN1C01price.iloc[:,1],ATMN1P01price.iloc[:,1]],axis=1) 
        ResultATMN101.index=ATMN1C01data.Times
        ResultATMN101.columns=['priceATMN101','callvolumeATMN101','putvolumeATMN101'] 
    else:
        ResultATMN101=pd.DataFrame(index=ATMC00data.Times,columns=['priceATMN101','callvolumeATMN101','putvolumeATMN101'])
    ResultATMN101['dayleft']=optioninfo01.iloc[0,4]
 
    
    #ATM+1,近期合约
    ATMP1C00data=w.wsi(optioninfo00ATMP1.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMP1P00data=w.wsi(optioninfo00ATMP1.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMP1C00price=pd.DataFrame(ATMP1C00data.Data)
    ATMP1P00price=pd.DataFrame(ATMP1P00data.Data)
    ATMP1C00price=ATMP1C00price.T
    ATMP1P00price=ATMP1P00price.T
    if ATMP1C00price.iloc[0,0]!='No Content': 
        FATMP100=(ATMP1C00price.iloc[:,0]-ATMP1P00price.iloc[:,0])*np.exp(0.05*t1)+optioninfo00ATMP1.iloc[0,1]
        ResultATMP100=pd.concat([FATMP100,ATMP1C00price.iloc[:,1],ATMP1P00price.iloc[:,1]],axis=1)   
        ResultATMP100.index=ATMP1C00data.Times
        ResultATMP100.columns=['priceATMP100','callvolumeATMP100','putvolumeATMP100']   
    else:
        ResultATMP100=pd.DataFrame(index=ATMC00data.Times,columns=['priceATMP100','callvolumeATMP100','putvolumeATMP100'])
    ResultATMP100['dayleft']=optioninfo00.iloc[0,4]
    
    
    'priceATMP100','callvolumeATMP100','putvolumeATMP100'
    #ATM+1,下期合约['priceATMP100','callvolumeATMP100','putvolumeATMP100'] 
    ATMP1C01data=w.wsi(optioninfo01ATMP1.iloc[0,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMP1P01data=w.wsi(optioninfo01ATMP1.iloc[1,0], "close,volume", start_time, end_time, "BarSize=5")
    ATMP1C01price=pd.DataFrame(ATMP1C01data.Data)
    ATMP1P01price=pd.DataFrame(ATMP1P01data.Data)
    ATMP1C01price=ATMP1C01price.T
    ATMP1P01price=ATMP1P01price.T
    if ATMP1C01price.iloc[0,0]!='No Content': 
        FATMP101=(ATMP1C01price.iloc[:,0]-ATMP1P01price.iloc[:,0])*np.exp(0.05*t2)+optioninfo01ATMP1.iloc[0,1]
        ResultATMP101=pd.concat([FATMP101,ATMP1C01price.iloc[:,1],ATMP1P01price.iloc[:,1]],axis=1)   
        ResultATMP101.index=ATMP1C01data.Times   
        ResultATMP101.columns=['priceATMP101','callvolumeATMP101','putvolumeATMP101']   
    else:
        ResultATMP101=pd.DataFrame(index=ATMC00data.Times,columns=['priceATMP101','callvolumeATMP101','putvolumeATMP101'])
    ResultATMP101['dayleft']=optioninfo01.iloc[0,4]

    Result1day=pd.concat([ResultATM00,ResultATM01,ResultATMN100,ResultATMN101,ResultATMP100,ResultATMP101],axis=1)
    result=pd.concat([result,Result1day],axis=0)
#    result.columns=['priceATM00','callvolumeATM00','putvolumeATM00','priceATM01','callvolumeATM01','putvolumeATM01','priceATMN100','callvolumeATMN100','putvolumeATMN100','priceATMN101','callvolumeATMN101','putvolumeATMN101','priceATMP100','callvolumeATMP100','putvolumeATMP100','priceATMP101','callvolumeATMP101','putvolumeATMP101']
result['ETFprice']=ETFprice
ETFclose=np.log(ETFclose)
ETFreturn=ETFclose.diff(1)
ETFvol=pd.Series(index=ETFreturn.index)
for i in range(len(ETFvol)):
    if i>=20:
        ETFvol[i]=np.std(ETFreturn[i-20:i])
    else:
        ETFvol[i]=0


#result.to_csv("bigdata.csv",index=True)
dealdata=result
#dealdata=pd.DataFrame.from_csv('E:/bigdata.csv')
dealdata.iloc[:,0]=dealdata.iloc[:,0]-dealdata.iloc[:,24]
dealdata.iloc[:,4]=dealdata.iloc[:,4]-dealdata.iloc[:,24]
dealdata.iloc[:,8]=dealdata.iloc[:,8]-dealdata.iloc[:,24]
dealdata.iloc[:,12]=dealdata.iloc[:,12]-dealdata.iloc[:,24] 
dealdata.iloc[:,16]=dealdata.iloc[:,16]-dealdata.iloc[:,24]
dealdata.iloc[:,20]=dealdata.iloc[:,20]-dealdata.iloc[:,24]
#result.to_csv("dealdata1111222.csv",index=True)
#
#dealdata=pd.DataFrame.from_csv('C:/Users/hasee/Desktop/python_workspace/guojin/dealdata1111.csv')
#ETFclose=pd.DataFrame.from_csv('C:/Users/hasee/Desktop/python_workspace/guojin/ETFclose.csv')
#ETFprice=pd.DataFrame.from_csv('C:/Users/hasee/Desktop/python_workspace/guojin/ETFprice.csv')

dealdata.iloc[:,3]=dealdata.iloc[:,3]/365*r*dealdata.iloc[:,24]
dealdata.iloc[:,7]=dealdata.iloc[:,7]/365*r*dealdata.iloc[:,24]
dealdata.iloc[:,11]=dealdata.iloc[:,11]/365*r*dealdata.iloc[:,24]
dealdata.iloc[:,15]=dealdata.iloc[:,15]/365*r*dealdata.iloc[:,24]
dealdata.iloc[:,19]=dealdata.iloc[:,19]/365*r*dealdata.iloc[:,24]
dealdata.iloc[:,23]=dealdata.iloc[:,23]/365*r*dealdata.iloc[:,24]

#
#dealdatamonday=dealdata[[x.isoweekday()==1 for x in dealdata.index]]
#dealdatafriday=dealdata[[x.isoweekday()==5 for x in dealdata.index]]

#ATM00std=pd.pivot_table(data,index=[data.index],aggfunc=np.std)
#for j in range(len(ATM00std)):
#    data[data.index==ATM00std.index[j]]=ATM00std.iloc[j,0]
    
    


#dealdata1=pd.DataFrame(dealdata.iloc[:,[0,3,24]])
#dealdata1['vol']=dealdata.iloc[:,24]
#data=dealdata1.to_period('D',inplace=True)
#for j in xrange(1,len(ETFvol)):
#    dealdata1['vol'][data.index==ETFvol.index[j]]=ETFvol[j]
#dealdata1=dealdata1[dealdata1['vol']!=0]
dealdata1=pd.DataFrame(dealdata.iloc[:,0])
dealdata1=dealdata1.to_period('D')
dealdata2=pd.DataFrame(dealdata.iloc[:,4])
dealdata3=pd.DataFrame(dealdata.iloc[:,8])
dealdata4=pd.DataFrame(dealdata.iloc[:,12])
dealdata5=pd.DataFrame(dealdata.iloc[:,16])
dealdata6=pd.DataFrame(dealdata.iloc[:,20])

 #折线图与成交量图一  
#plt.figure()
#ax1=plt.subplot(211)
#N=len(dealdatamonday.iloc[:,0])
#ind=np.arange(len(dealdatamonday.iloc[:,0]))
#ax1.plot(ind,dealdatamonday.iloc[:,0]-dealdatamonday.iloc[:,3],label='ATM00')#减去资金成本
##ax1.plot(ind,dealdata1.iloc[:,0]*1000)#不减去资金成本
##ax1.plot(ind,dealdata1.iloc[:,1]*1000)
#def format_date(x, pos=None):
#    thisind=np.clip(int(x+0.5), 0, N-1)
#    #thisind=int(np.round(x))#保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
#    return dealdatamonday.index[thisind]
#ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
##fig.autofmt_xdate() 
#plt.legend()
#ax1.grid()
#
#ax2=plt.subplot(212)
#N=len(dealdatafriday.iloc[:,0])
#ind=np.arange(len(dealdatafriday.iloc[:,0]))
#ax2.plot(ind,dealdatafriday.iloc[:,0]-dealdatafriday.iloc[:,3],label='ATM00')#减去资金成本
##ax1.plot(ind,dealdata1.iloc[:,0]*1000)#不减去资金成本
##ax1.plot(ind,dealdata1.iloc[:,1]*1000)
#def format_date(x, pos=None):
#    thisind=np.clip(int(x+0.5), 0, N-1)
#    #thisind=int(np.round(x))#保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
#    return dealdatafriday.index[thisind]
#ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
##fig.autofmt_xdate() 
#plt.legend()
#ax2.grid()
##ax3=ax1.twinx()
##ax3.plot(ind,dealdata.iloc[:,24],'red')
#
#ax2=plt.subplot(212)
#ax2.plot(ind,dealdata.iloc[:,2],'red')
#ax3=ax2.twinx()
#ax3.plot(ind,np.sqrt(244)*dealdata1.iloc[:,3])
#ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
#ax1.set_title("ATM00 ETFprice")
#ax2.grid()



#
#ATM00bar=pd.pivot_table(data,values=['callvolumeATM00','putvolumeATM00'],index=[data.index],aggfunc=np.sum)
#ATM00barplot=ATM00bar.iloc[:,0]+ATM00bar.iloc[:,1]
##ATM00bar.plot(kind='bar'ax=ax2)
#ax2.bar(ATM00barplot.index.to_timestamp(),ATM00barplot)
#fig.autofmt_xdate()  # 自动格式化日期，防止其溢出绘图区域


###K线图1
twenty25=pd.pivot_table(dealdata1,index=[dealdata1.index],aggfunc=lambda x:np.percentile(x,25))
seventy75=pd.pivot_table(dealdata1,index=[dealdata1.index],aggfunc=lambda x:np.percentile(x,75))
maxx=pd.pivot_table(dealdata1,index=[dealdata1.index],aggfunc=np.max)
minn=pd.pivot_table(dealdata1,index=[dealdata1.index],aggfunc=np.min)
#volume=pd.pivot_table(dealdata,values=['callvolumeATM00','putvolumeATM00'],index=[dealdata.index],aggfunc=np.sum)
#volumee=pd.DataFrame(volume.iloc[:,0]+volume.iloc[:,1])






####sss = date2num(maxx.index.to_timestamp().date)  将DATAframe格式转化为num格式
plt.figure()
ax1=plt.subplot(111)
N=len(maxx)
candle=pd.concat([pd.DataFrame(np.arange(len(maxx)),index=maxx.index),twenty25*1000,maxx*1000,minn*1000,seventy75*1000],axis=1)
stock_array=np.array(candle)
zero=pd.DataFrame(np.zeros((len(stock_array),1)),index=stock_array[:,0])
candlestick_ohlc(ax1, stock_array, colorup = "red", colordown="green", width=0.2)
ax1.plot(zero)
#mpf.plot_day_summary_oclh(ax1, stock_array, colorup = "red", colordown="green")
ax2=ax1.twinx()
ax2.plot(pd.DataFrame(np.arange(len(maxx))),ETFclose[1:-1])
def format_date(x, pos=None):
    thisind=np.clip(int(x+0.5), 0, N-1)
    #thisind=int(np.round(x))#保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
    return maxx.index[thisind]
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
#ax1.xaxis_date() 

ax1.set_title("ATM00 ETFprice")


plt.figure()
ax1=plt.subplot(111)
N=len(maxx)
candle=pd.concat([pd.DataFrame(np.arange(len(maxx)),index=maxx.index),twenty25*1000,maxx*1000,minn*1000,seventy75*1000],axis=1)
stock_array=np.array(candle)
zero=pd.DataFrame(np.zeros((len(stock_array),1)),index=stock_array[:,0])
candlestick_ohlc(ax1, stock_array, colorup = "red", colordown="green", width=0.2)
ax1.plot(zero)
#mpf.plot_day_summary_oclh(ax1, stock_array, colorup = "red", colordown="green")
ax2=ax1.twinx()
ax2.plot(pd.DataFrame(np.arange(len(maxx))),ETFvol[1:-1])
def format_date(x, pos=None):
    thisind=np.clip(int(x+0.5), 0, N-1)
    #thisind=int(np.round(x))#保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
    return maxx.index[thisind]
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
#ax1.xaxis_date() 

ax1.set_title("ATM00 ETFvol")
###

###将DataFrame中的时间数据转为可读的数据，需要matplotlib.dates（mdates） 和datetime（dt）
# convert the datetime64 column in the dataframe to 'float days'
 #daysreshape['DateTime']=mdates.date2num(daysreshape['DateTime'].astype(dt.date))



###Fprice1.describe()   取25 50 75 分位数的简单方法

###话热力图
#
#Fprice1=pd.DataFrame()
#Fprice2=pd.DataFrame()
#Fprice3=pd.DataFrame()
#Fprice4=pd.DataFrame()
#Fprice5=pd.DataFrame()
#Fprice6=pd.DataFrame()
#
#for i in range(0,len(ETFclose)):
#    dayprice1=data1[data1.index==ETFclose.index[i]]
#    dayprice1.index=range(len(dayprice1))  
#    Fprice1=pd.concat([Fprice1,dayprice1],axis=1)
#    
#    dayprice2=data2[data2.index==ETFclose.index[i]]
#    dayprice2.index=range(len(dayprice2))  
#    Fprice2=pd.concat([Fprice2,dayprice2],axis=1)
#    
#    dayprice3=data3[data3.index==ETFclose.index[i]]
#    dayprice3.index=range(len(dayprice3))  
#    Fprice3=pd.concat([Fprice3,dayprice3],axis=1)
#
#    dayprice4=data4[data4.index==ETFclose.index[i]]
#    dayprice4.index=range(len(dayprice4))  
#    Fprice4=pd.concat([Fprice4,dayprice4],axis=1)
#
#    dayprice5=data5[data5.index==ETFclose.index[i]]
#    dayprice5.index=range(len(dayprice5))  
#    Fprice5=pd.concat([Fprice5,dayprice5],axis=1)
#    
#    dayprice6=data6[data6.index==ETFclose.index[i]]
#    dayprice6.index=range(len(dayprice6))  
#    Fprice6=pd.concat([Fprice6,dayprice6],axis=1)
#    
#Fprice1.columns=ETFclose.to_period('D').index
#Fprice2.columns=ETFclose.index
#Fprice3.columns=ETFclose.index
#Fprice4.columns=ETFclose.index
#Fprice5.columns=ETFclose.index
#Fprice6.columns=ETFclose.index
#
#Fprice1=Fprice1.dropna(axis=0,how='all')
#Fprice2=Fprice2.dropna(axis=0,how='all')
#Fprice3=Fprice3.dropna(axis=0,how='all')
#Fprice4=Fprice4.dropna(axis=0,how='all')
#Fprice5=Fprice5.dropna(axis=0,how='all')
#Fprice6=Fprice6.dropna(axis=0,how='all')
#plt.figure()
#ax1=plt.subplot(111)
#import seaborn as sns
#import matplotlib.cm as cm
#ax1.
#sns.heatmap(Fprice1*1000,square=True,cmap=cm.blue)
#
