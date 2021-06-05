# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 18:59:42 2021

@author: eljuan
"""


import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

# Get financial data
ric = 'DBK.DE'
table_raw = pd.read_csv()


# Input for jarque bera
x = None # Returns
title_x = None # 
siz = None # 


# Compute "risk metrics"
x_mean = np.mean(x)
x_stdev = np.std(x)
x_skew = skew(x)
x_kurt = kurtosis(x)
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
print('stdev = ' + str(x_stdev))
print('Skewness = ' + str(x_skew))
print('Kurtosis = ' + str(x_kurt))
print('Median = ' + str(x_median))
print('VaR 95% = ' + str(x_VaR_95))
print('CVaR 95% = ' + str(x_CVaR_95))
print('test Jarque-Bera = ' + str(jb))
print('p_value = '+str(p_value))
print('Is normal: '+ str(is_normal))


# PLot histograms
plt.figure()
plt.hist(x,bins=100)
plt.title("Histogram "+ title_x)   
plt.show()
