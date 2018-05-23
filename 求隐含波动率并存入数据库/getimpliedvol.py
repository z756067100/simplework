# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:56:41 2018

@author: hasee
"""

import numpy as np
from scipy import stats
from scipy.optimize import newton
def getimpliedvolC(opt_price,stockprice,strike,T,r):
#    opt_price=24
#    strike=102
#    stockprice=100
#    T=1
#    r=0.05
#    sigma=0.46
    def Eu_optioncall(sigma):
        d1=(np.log(float(stockprice)/strike)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
        d2=d1-sigma*np.sqrt(T)
        C=stockprice*stats.norm.cdf(d1)-strike*stats.norm.cdf(d2)*np.exp(-r*T)
        vega=stockprice*np.sqrt(T)*stats.norm.pdf(d1)
        return C-opt_price
    if T==0:
        return 0
    else:
        return newton(Eu_optioncall,0.3,tol=1.48e-08,maxiter=50)
getimpliedvolC(19.45,100,102,1,0.05)


def getimpliedvolP(opt_price,stockprice,strike,T,r):
#    opt_price=24
#    strike=102
#    stockprice=100
#    T=1
#    r=0.05
#    sigma=0.46
    if T==0:
        return 0
    else:        
        def Eu_optionput(sigma):
            d1=(np.log(float(stockprice)/strike)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
            d2=d1-sigma*np.sqrt(T)
            P=strike*stats.norm.cdf(-d2)*np.exp(-r*T)-stockprice*stats.norm.cdf(-d1)
            vega=stockprice*np.sqrt(T)*stats.norm.pdf(d1)
            return P-opt_price
        return newton(Eu_optionput,0.3,tol=1.48e-08,maxiter=50)#,fprime=lambda sigma:vega)此处是死循环，要有sigma才能求vega，但是我们是求sigma


getimpliedvolC(0.0707,3.173,3.1,1.0/365,0.048)
getimpliedvolP(10,102,102,1,0.05)
