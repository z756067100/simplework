# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 10:18:03 2018

@author: hasee
"""

import numpy as np
import pandas as pd
from WindPy import w
import getimpliedvol as gv
from sqlalchemy import create_engine
w.start()
r=0.048
w_wsdETF=w.wsd("510050.SH", "close", "2018-01-22", "2018-01-23", "")
ETFclose=pd.Series(w_wsdETF.Data[0],index=w_wsdETF.Times)



db_info = {'user': 'root',
           'password': 'yongyuan6nian3',
           'host': 'localhost',
           'port': 3306}
engine = create_engine('mysql+mysqldb://%(user)s:%(password)s@%(host)s:%(port)s' % db_info)


## 利用50ETF价格来判断ATM的期权
result=pd.DataFrame()
for i in xrange(1,len(ETFclose)):
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
## 找到ATM+-2
    ups=np.abs(optioninfo.iloc[:,1]-ETFclose[i-1])
    optioninfo['type']=None
    optioninfo['type'][optioninfo[ups==np.min(ups)].index]='ATM'
    optioninfo['type'][optioninfo[ups==np.min(ups)].index+1]='ATM+1'
    optioninfo['type'][optioninfo[ups==np.min(ups)].index+2]='ATM+2'  
    optioninfo['type'][optioninfo[ups==np.min(ups)].index-1]='ATM-1'
    optioninfo['type'][optioninfo[ups==np.min(ups)].index-2]='ATM-2'
    optioninfo=optioninfo[optioninfo.iloc[:,6].values!=None]
## 找到00，01属性    
    optioninfo['kind']=None
    optioninfo.iloc[:,2]==T.strftime('%Y%m')## 利用字符串在每个月末换期的时候会出现问题
    optioninfo['kind'][optioninfo.iloc[:,2]==optioninfo.iloc[0,2]]=['00']
    optioninfo['kind'][optioninfo.iloc[:,2]==(optioninfo.iloc[0,2]+1)]=['01']    
    optioninfo=optioninfo[optioninfo.iloc[:,7].values!=None]    

## 找到当日期权价格和标的价格
    w_wsdoption=w.wsd(optioninfo['Code'].tolist(), "close", T, T, "")
    optioninfo['price']=w_wsdoption.Data[0]  
    optioninfo['ETFprice']=ETFclose[i]  

   
## 反求隐含波动率
    optioninfo['vol']=None
    optioninfo.reset_index(inplace=True)
    optioninfo.drop(optioninfo.columns[0],axis=1,inplace=True)
    for j in range(len(optioninfo)):
        if optioninfo['C or P'][j]==u'认购':
            optioninfo['vol'][j]=gv.getimpliedvolC(optioninfo['price'][j],
                      optioninfo['ETFprice'][j],optioninfo['K'][j],
                      optioninfo['T_days'][j]/365.0,r)
        else:
            optioninfo['vol'][j]=gv.getimpliedvolP(optioninfo['price'][j],
                      optioninfo['ETFprice'][j],optioninfo['K'][j],
                      optioninfo['T_days'][j]/365.0,r)
    optionC=optioninfo[optioninfo['C or P']==u'认购']
    optionC.reset_index(inplace=True)
    optionC.drop(optionC.columns[0],axis=1,inplace=True)
    optionP=optioninfo[optioninfo['C or P']==u'认沽']
    optionP.reset_index(inplace=True)
    optionP.drop(optionP.columns[0],axis=1,inplace=True)
    optionCP=optionC.iloc[:,[1,2,4,5,6,7,9,10]]
    optionCP['vol']=(optionC['vol']+optionP['vol'])/2.0
    result=pd.concat([result,optionCP],axis=0)
    
pd.io.sql.to_sql(result,'vol555', engine, schema='volsurface', if_exists='append')  

