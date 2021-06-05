# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 20:55:06 2021

@author: eljua
"""


import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2


'''
Create a normility test using random variables
Visualizar histograma

'''
# Play with Borel-Cantelli 
# is_normal = True
# counter = 0
# while is_normal:

siz = 10**6
df = 2
type_random_variable = "normal" # exponential normal student

if type_random_variable == "normal":
    x = np.random.standard_normal(siz)
    title_x = type_random_variable
elif type_random_variable == "exponential":
    x = np.random.standard_exponential(siz)
    title_x = type_random_variable
elif type_random_variable == "student":
    x = np.random.standard_t(df,siz)
    title_x = type_random_variable + ' (df = ' + str(df) + ')'
elif type_random_variable == "ChiSquared":
    x = np.random.chisquare(df,siz)
    title_x = type_random_variable + ' (df = ' + str(df) + ')'
    

# Compute "risk metrics"
x_mean = np.mean(x)
x_stdev = np.std(x)
x_skew = skew(x)
x_kurt = kurtosis(x) # si fisher=False se debe restar '3.0' en 'jb' a 'kurt'
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

# print('counter = ' + str(counter))
# print('-------')
# counter += 1


















