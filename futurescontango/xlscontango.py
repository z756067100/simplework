# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 08:24:01 2018

@author: hasee
"""


import xlwings as xw
import time
from WindPy import w
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from scipy import interpolate
np.interp

w.start()

def draw():
    wb=xw.Book.caller()
#    wb=xw.books.active
    sht=wb.sheets[0]
    sht_data=wb.sheets['data']
    start=str(sht.range('B1').value)
    end=str(sht.range('B2').value)
    start_day=time.strftime('%Y-%m-%d',time.strptime(start,'%Y-%m-%d %H:%M:%S'))
    end_day=time.strftime('%Y-%m-%d',time.strptime(end,'%Y-%m-%d %H:%M:%S'))
    quantile1=sht.range('B5').value
    quantile2=sht.range('B6').value
#    wb=xw.books.active
#    sht=wb.sheets[0]
    ex_day=sht.range('B4').options(numbers=int).value
    kind=sht.range('B3').value

    if kind=='IF':
        w_wsi300=w.wsi("000300.SH", "close",start, end, "BarSize=15")
        price300=pd.DataFrame(w_wsi300.Data,columns=w_wsi300.Times,index=w_wsi300.Codes)                    #沪深300指数信息
        price300=price300.T
        ##获得00信息
        w_wsi=w.wsi("IF00.CFE", "close", start, end, "BarSize=15")
        IF00=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IF00=IF00.T
                    
        w_wsd=w.wsd("IF00.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T  

        Code['newcol1'] = Code[0].apply(lambda x: duedate.loc[x, 0])   #此处0是列标签 
        IF00['exday']=Code.loc[IF00.index.date,'newcol1'].tolist()                  
        IF00['remaining day']=(IF00.iloc[:,1]-IF00.index.date)
        IF00.iloc[:,2]=[x.days for x in IF00.iloc[:,2]]
            
        ##获得01信息
        w_wsi=w.wsi("IF01.CFE", "close", start, end, "BarSize=15")
        IF01=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IF01=IF01.T 

         
        w_wsd=w.wsd("IF01.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IF01['exday']=Code.loc[IF01.index.date,'newcol1'].tolist()                  
        IF01['remaining day']=(IF01.iloc[:,1]-IF01.index.date)
        IF01.iloc[:,2]=[x.days for x in IF01.iloc[:,2]]
                        
        ##获得02信息
        w_wsi=w.wsi("IF02.CFE", "close", start, end, "BarSize=15")
        IF02=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IF02=IF02.T 

         
        w_wsd=w.wsd("IF02.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IF02['exday']=Code.loc[IF02.index.date,'newcol1'].tolist()                  
        IF02['remaining day']=(IF02.iloc[:,1]-IF02.index.date)
        IF02.iloc[:,2]=[x.days for x in IF02.iloc[:,2]]
        
        ##获得03消息
        w_wsi=w.wsi("IF03.CFE", "close", start, end, "BarSize=15")
        IF03=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IF03=IF03.T 

         
        w_wsd=w.wsd("IF03.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IF03['exday']=Code.loc[IF03.index.date,'newcol1'].tolist()                  
        IF03['remaining day']=(IF03.iloc[:,1]-IF03.index.date)
        IF03.iloc[:,2]=[x.days for x in IF03.iloc[:,2]]
        
        xp=pd.concat([IF00.iloc[:,2],IF01.iloc[:,2],IF02.iloc[:,2],IF03.iloc[:,2]],axis=1)
        yp=pd.concat([IF00.iloc[:,0],IF01.iloc[:,0],IF02.iloc[:,0],IF03.iloc[:,0]],axis=1)   
        exday=pd.Series(np.arange(len(xp)),index=xp.index)
        exday[:]=ex_day
        result=pd.Series(index=xp.index)
        for i in range(len(result)):          
            result[i]=np.interp(exday[i],xp.iloc[i,:],yp.iloc[i,:])   
        result=(result-price300.iloc[:,0])/price300.iloc[:,0]*365/ex_day
        result.dropna(axis=0,how='any',inplace=True)  
                             
   

    if kind=='IC':

        w_wsi500=w.wsi("000905.SH", "close",start, end, "BarSize=15")
        price500=pd.DataFrame(w_wsi500.Data,columns=w_wsi500.Times)                    #沪深300指数信息
        price500=price500.T
        

        w_wsi=w.wsi("IC00.CFE", "close", start, end, "BarSize=15")
        IC00=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC00=IC00.T
                    
        w_wsd=w.wsd("IC00.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T  

        Code['newcol1'] = Code[0].apply(lambda x: duedate.loc[x, 0])   #此处0是列标签 
        IC00['exday']=Code.loc[IC00.index.date,'newcol1'].tolist()                  
        IC00['remaining day']=(IC00.iloc[:,1]-IC00.index.date)
        IC00.iloc[:,2]=[x.days for x in IC00.iloc[:,2]]
            
            ##获得01信息
        w_wsi=w.wsi("IC01.CFE", "close", start, end, "BarSize=15")
        IC01=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC01=IC01.T 

         
        w_wsd=w.wsd("IC01.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC01['exday']=Code.loc[IC01.index.date,'newcol1'].tolist()                  
        IC01['remaining day']=(IC01.iloc[:,1]-IC01.index.date)
        IC01.iloc[:,2]=[x.days for x in IC01.iloc[:,2]]

            
            
        ##获得02信息
        w_wsi=w.wsi("IC02.CFE", "close", start, end, "BarSize=15")
        IC02=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC02=IC02.T 

         
        w_wsd=w.wsd("IC02.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC02['exday']=Code.loc[IC02.index.date,'newcol1'].tolist()                  
        IC02['remaining day']=(IC02.iloc[:,1]-IC02.index.date)
        IC02.iloc[:,2]=[x.days for x in IC02.iloc[:,2]]
           
        ##获得03消息
        w_wsi=w.wsi("IC03.CFE", "close", start, end, "BarSize=15")
        IC03=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC03=IC03.T 

         
        w_wsd=w.wsd("IC03.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC03['exday']=Code.loc[IC03.index.date,'newcol1'].tolist()                  
        IC03['remaining day']=(IC03.iloc[:,1]-IC03.index.date)
        IC03.iloc[:,2]=[x.days for x in IC03.iloc[:,2]]

        xp=pd.concat([IC00.iloc[:,2],IC01.iloc[:,2],IC02.iloc[:,2],IC03.iloc[:,2]],axis=1)
        yp=pd.concat([IC00.iloc[:,0],IC01.iloc[:,0],IC02.iloc[:,0],IC03.iloc[:,0]],axis=1)   
        exday=pd.Series(np.arange(len(xp)),index=xp.index)
        exday[:]=ex_day
        result=pd.Series(index=xp.index)
        for i in range(len(result)):          
            result[i]=np.interp(exday[i],xp.iloc[i,:],yp.iloc[i,:])   
        result=(result-price500.iloc[:,0])/price500.iloc[:,0]*365/ex_day
        result.dropna(axis=0,how='any',inplace=True)   
        
    if kind=='IH':
            ##获得00信息
        w_wsi050=w.wsi("000016.SH", "close",start, end, "BarSize=15")
        price050=pd.DataFrame(w_wsi050.Data,columns=w_wsi050.Times)                    #沪深300指数信息
        price050=price050.T
        
    ##获得00信息
        w_wsi=w.wsi("IH00.CFE", "close", start, end, "BarSize=15")
        IC00=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC00=IC00.T
                    
        w_wsd=w.wsd("IH00.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T  

        Code['newcol1'] = Code[0].apply(lambda x: duedate.loc[x, 0])   #此处0是列标签 
        IC00['exday']=Code.loc[IC00.index.date,'newcol1'].tolist()                  
        IC00['remaining day']=(IC00.iloc[:,1]-IC00.index.date)
        IC00.iloc[:,2]=[x.days for x in IC00.iloc[:,2]]

        ##获得01信息
        w_wsi=w.wsi("IH01.CFE", "close", start, end, "BarSize=15")
        IC01=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC01=IC01.T 

         
        w_wsd=w.wsd("IH01.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC01['exday']=Code.loc[IC01.index.date,'newcol1'].tolist()                  
        IC01['remaining day']=(IC01.iloc[:,1]-IC01.index.date)
        IC01.iloc[:,2]=[x.days for x in IC01.iloc[:,2]]
        
        
        ##获得02信息
        w_wsi=w.wsi("IH02.CFE", "close", start, end, "BarSize=15")
        IC02=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC02=IC02.T 

         
        w_wsd=w.wsd("IH02.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC02['exday']=Code.loc[IC02.index.date,'newcol1'].tolist()                  
        IC02['remaining day']=(IC02.iloc[:,1]-IC02.index.date)
        IC02.iloc[:,2]=[x.days for x in IC02.iloc[:,2]]
                                   
            
        ##获得03信息
        w_wsi=w.wsi("IH03.CFE", "close", start, end, "BarSize=15")
        IC03=pd.DataFrame(w_wsi.Data,columns=w_wsi.Times,index=w_wsi.Codes)
        IC03=IC03.T 

         
        w_wsd=w.wsd("IH03.CFE", "trade_hiscode", start_day, end_day, "")
        Code=pd.DataFrame(w_wsd.Data,columns=w_wsd.Times)
        Code=Code.T

        s=[str(x) for x in Code.iloc[:,0]]
        w_wss=w.wss(list(set(s)), "lastdelivery_date")           
        duedate=pd.DataFrame(w_wss.Data,columns=w_wss.Codes)
        duedate=duedate.T                        
        
        Code['newcol1'] = Code.iloc[:,0].apply(lambda x: duedate.loc[x, 0])    
        IC03['exday']=Code.loc[IC03.index.date,'newcol1'].tolist()                  
        IC03['remaining day']=(IC03.iloc[:,1]-IC03.index.date)
        IC03.iloc[:,2]=[x.days for x in IC03.iloc[:,2]]
            
        xp=pd.concat([IC00.iloc[:,2],IC01.iloc[:,2],IC02.iloc[:,2],IC03.iloc[:,2]],axis=1)
        yp=pd.concat([IC00.iloc[:,0],IC01.iloc[:,0],IC02.iloc[:,0],IC03.iloc[:,0]],axis=1)   
        exday=pd.Series(np.arange(len(xp)),index=xp.index)
        exday[:]=ex_day
        result=pd.Series(index=xp.index)
        for i in range(len(result)):          
            result[i]=np.interp(exday[i],xp.iloc[i,:],yp.iloc[i,:])   
        result=(result-price050.iloc[:,0])/price050.iloc[:,0]*365/ex_day
        result.dropna(axis=0,how='any',inplace=True) 

    sht_data.range('A1').expand().clear_contents()
    sht_data.range('A1').options(index=True, header=False).value=result   
        
  
        
    N=len(result)
    name=np.random.normal()
    fig=plt.figure(str(name),figsize=(8,4))   
    plt.axhline(np.percentile(result,quantile1*100),color='black',
                linestyle="--",label=str(quantile1))
    plt.axhline(np.percentile(result,quantile2*100),color='black',
                linestyle="-.",label=str(quantile2))   

    plt.annotate('%.4f' %np.percentile(result,25),xy=(0,np.percentile(result,25)))
    plt.annotate('%.4f' %np.percentile(result,75),xy=(600,np.percentile(result,75)))
    plt.plot(np.arange(N),result,label=str(ex_day))
    def format_date(x, pos=None):
        thisind=np.clip(int(x+0.5), 0, N-1)
        return result.index.date[thisind]
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_date)) 
    plt.grid()
    plt.gca().set_title(str(kind),fontsize=15)
#    plt.legend()
    plt.legend(loc=0, fontsize=10)
    plt.xticks(fontsize=10)
    plt.xticks(rotation=30)
    plt.yticks(fontsize=10)
    sht.pictures.add(fig, name=str(name), update=False,left=sht.range('C30').left, top=sht.range('B7').top)
#    plot1.height=4.3
#    plot1.width=3.2

#    学习画图
#    import matplotlib.pyplot as plt
#import numpy as np
#x = np.arange(0,6)
#y = x * x
# 
#plt.plot(x, y, marker='o')
#for xy in zip(x,y):
#    plt.annotate("(%s,%s)" % xy, xy=xy, xytext=(-20,10), textcoords = 'offset points')

