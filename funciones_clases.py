# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 01:45:43 2021

@author: eljua
"""


# Import libraries
import numpy as np
import pandas as pd
# import matplotlib as mpl
# import scipy
# import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

# Input

ric = 'SGRE.MC' # ^VIX MXN=X ^IXIC DBK.DE ^STOXX CL=F SGRE.MC 
file_extension = '.csv'
# Get financial data

path = 'C:\\Users\\eljua\\.spyder-py3\\FC\\DATA\\'+ ric + file_extension
table_raw = pd.read_csv(path)

# Create table of returns
t = pd.DataFrame()
t['date'] = pd.to_datetime(table_raw['Date'],dayfirst = True)
t['close'] = table_raw['Close']
t['close_pre'] = table_raw['Close'].shift(1)
t['returns'] = t['close']/t['close_pre'] - 1
t = t.dropna()
t = t.reset_index(drop=True)

# Input for jarque bera
x = t['returns'].values # Returns
title_x = 'Returns ' + ric # 

# Prices plot
plt.figure()
plt.plot(t['date'],t['close'])
plt.ylabel('Price')
plt.xlabel('Time')
plt.title(title_x)
plt.show()

# Compute "risk metrics"
siz = len(x)
x_mean = np.mean(x)
x_std = np.std(x)
x_skew = skew(x)
x_kurt = kurtosis(x)
x_sharpe = x_mean/x_std * np.sqrt(252) # annualized
x_median = np.percentile(x,97.5)
x_VaR_95 = np.percentile(x,5)
x_CVaR_95 = np.mean(x[x <= x_VaR_95])
jb = siz/6*(x_skew**2 + 1/4*x_kurt**2)
p_value = 1 - chi2.cdf(jb,df=2)
is_normal = (p_value > 0.05)

# jb = (siz/6)*(x_skew**2 + (1/4)*(x_kurt-3)**2) 


# Print metrics
print(title_x)
print('mean = ' + str(x_mean))
print('stdev = ' + str(x_std))
print('Skewness = ' + str(x_skew))
print('Kurtosis = ' + str(x_kurt))
print('Sharpe = ' + str(x_sharpe))
print('Median = ' + str(x_median))
print('VaR 95% = ' + str(x_VaR_95))
print('CVaR 95% = ' + str(x_CVaR_95))
print('test Jarque-Bera = ' + str(jb))
print('p_value = '+str(p_value))
print('Is normal: '+ str(is_normal))

# Print metrics on graph

# Print metrics
round_digits = 4
plt_str = 'mean = ' + str(np.round(x_mean,round_digits))\
    + '/ (stdev = ' + str(np.round(x_std,round_digits))\
    + '/ Skewness = ' + str(np.round(x_skew,round_digits))\
    + '/ Kurtosis = ' + str(np.round(x_kurt,round_digits))\
    + '/ Sharpe = ' + str(np.round(x_sharpe,round_digits))\
    + '/ Median = ' + str(np.round(x_median,round_digits)) + '\n'\
    + '/ VaR 95% = ' + str(np.round(x_VaR_95,round_digits))\
    + '/ CVaR 95% = ' + str(np.round(x_CVaR_95,round_digits))\
    + '/ test Jarque-Bera = ' + str(np.round(jb,round_digits))\
    + '/ p_value = ' +str(np.round(p_value,round_digits))\
    + '/ Is normal: ' + str(is_normal)

# PLot histograms
plt.figure()
plt.hist(x,bins=100)
plt.title("Histogram "+ title_x) 
plt.xlabel(plt_str)  
plt.show()
