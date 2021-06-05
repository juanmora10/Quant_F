# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 01:48:55 2021

@author: eljua
"""

# Import libraries
import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2
from scipy.optimize import minimize
from numpy import linalg as LA


def load_ts(ric, file_extension='.csv'):

    path = 'C:\\Users\\eljua\\.spyder-py3\\FC\\DATA\\'+ ric + file_extension    
    # Input
    # Get financial data   
    if file_extension == '.csv':
        table_raw = pd.read_csv(path)
    else:
        table_raw = pd.read_excel(path)
        
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
    title = 'Returns ' + ric # 
           
    return x, title, t

def plot_ts(t,ric,title):

    # Prices plot
    plt.figure()
    plt.plot(t['date'],t['close'])
    plt.ylabel('Price')
    plt.xlabel('Time')
    plt.title(title)
    plt.show()
    
    
def plot_hist(x, title,plt_str):
    
    # PLot histograms
    plt.figure()
    plt.hist(x,bins=100)
    plt.title("Histogram "+ title) 
    plt.xlabel(plt_str)  
    plt.show()

# Funciones para CAPM

def sinchronise_timeseries(ric, bmk):

    # load timeseries
    x, title, t = load_ts(ric)
    x1, title1, t1 = load_ts(bmk)   
        
    # sinchronaise timeseries
    timestamps = list(set(list(t['date'].values)) & set(list(t1['date'].values)))
    
    t_n = t[t['date'].isin(timestamps)]
    t_n.sort_values(by= 'date', ascending = True)
    t_n = t_n.reset_index(drop=True)
    
    t1_n = t1[t1['date'].isin(timestamps)]
    t1_n.sort_values(by= 'date', ascending = True)
    t1_n = t1_n.reset_index(drop=True) 
    
    # create a new dataframe
    t = pd.DataFrame()
    t['date'] = timestamps
    t[str(ric + ' close')] = t_n['close']
    t[str(bmk + ' close')] = t1_n['close']
    t[str(ric + ' returns')] = t_n['returns']
    t[str(bmk + ' returns')] = t1_n['returns']
    
    # compute vectors 
    
    y = t[ric + ' returns'].values
    x = t[bmk + ' returns'].values
    
    return x, y, t

    
    
    