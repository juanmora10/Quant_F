# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 14:50:47 2021

@author: eljua
"""

# Importar librerias

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2, linregress
from scipy.optimize import minimize
from numpy import linalg as LA


# Import own files
import stream_functions as sf
importlib.reload(sf)
import stream_clases as sc
importlib.reload(sc)

ric = 'DBK.DE'
bmk = '^IXIC'

x, title, t = sf.load_ts(ric)
x1, title1, t1 = sf.load_ts(bmk)

nb_decimals = 4

#   x1 = alpha + beta*x2 + epsilon

##   sincronizar timestamps cuando las observaciones son diferentes en cada
##   data frame. En este caso ambas tenian las mismas, sin embargo se sincronizó

# seleccionar la fecha de cada serie
# convertir en lista
# con set convertir en un conjunto y con & intercección con otro consjunto
# convertir en lista

timestamps = list(set(list(t['date'].values)) & set(list(t1['date'].values)))

##   sincronizar para x y x1

t_n = t[t['date'].isin(timestamps)]
t_n.sort_values(by= 'date', ascending = True)
t_n = t_n.reset_index(drop=True)

t1_n = t1[t1['date'].isin(timestamps)]
t1_n.sort_values(by= 'date', ascending = True)
t1_n = t1_n.reset_index(drop=True) 

t = pd.DataFrame()
t['date'] = timestamps
t[ric + ' close'] = t_n['close']
t[bmk + ' close'] = t1_n['close']
t[ric + ' returns'] = t_n['returns']
t[bmk + ' returns'] = t1_n['returns']

# compute vectors 

y = t[ric + ' returns'].values
x = t[bmk + ' returns'].values

# linear Regression

slope, intercept, r_value, p_value, std_err = linregress(x,y)
slope = np.round(slope, nb_decimals)
intercept = np.round(intercept, nb_decimals)
p_value = np.round(p_value, nb_decimals)
null_hypothesis = p_value > 0.05
r_value = np.round(r_value, nb_decimals)
r_squared = np.round(r_value**2, nb_decimals)
predictor_linreg = slope*x + intercept*x

# Scatterplot of returns

str_title = 'Scatterplot of returns ' + '\n'\
    + 'Linear regression / ric ' + ric\
    + '/ Benchmark ' + bmk + '\n'\
    + 'alpha (intercept) ' + str(intercept)\
    + '/ beta (slope) ' + str(slope) + '\n'\
    + 'p_value ' + str(p_value)\
    + '/ null hypothesis ' + str(null_hypothesis) + '\n'\
    + 'r_value ' + str(r_value)\
    + '/ r_squared ' + str(r_squared)
plt.figure()
plt.title(str_title)
plt.scatter(x,y)
plt.plot(x,predictor_linreg, color='red')
plt.ylabel(ric)
plt.xlabel(bmk)
plt.grid()
plt.show










