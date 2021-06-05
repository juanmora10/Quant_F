# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 11:42:37 2021

@author: eljua
"""
# Import libraries
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

class jarque_bera_test():
    
    def __init__(self,ric):
        
        self.ric = ric
        self.returns = []
        self.str_title = None
        self.size = 0
        self.returns_digits = 4
        self.mean = 0.0
        self.std = 0.0
        self.skew = 0.0
        self.kurt = 0.0
        self.sharpe =0.0
        self.median = 0.0
        self.VaR_95 = 0.0
        self.CVaR_95 = 0.0
        self.jarque_bera = 0.00
        self.p_value = 0.0
        self.is_normal = 0.0
        
    def __str__(self):
        metrics_str = self.str_title + ' ' + '/ Size = ' + str(self.size) + '\n' + str(self.plt_str())
        return metrics_str
    
    def load_timeseries(self):
        # Load and sinchronise timeseries
        self.returns, self.str_title, self.t = sf.load_ts(self.ric)
        self.size = len(self.returns)
    
    def compute(self):
    
        self.mean = np.mean(self.returns)
        self.std = np.std(self.returns)
        self.skew = skew(self.returns)
        self.kurt = kurtosis(self.returns)
        self.sharpe = self.mean/self.std * np.sqrt(252) # annualized
        self.median = np.percentile(self.returns,97.5)
        self.VaR_95 = np.percentile(self.returns,5)
        self.CVaR_95 = np.mean(self.returns[self.returns <= self.VaR_95])
        self.jarque_bera = self.size/6*(self.skew**2 + 1/4*self.kurt**2)
        self.p_value = 1 - chi2.cdf(self.jarque_bera,df=2)
        self.is_normal = (self.p_value > 0.05)
                
    def plt_str(self):        
        round_digits = 4
        plt_str = 'mean = ' + str(np.round(self.mean,round_digits))\
            + '/ stdev = ' + str(np.round(self.std,round_digits))\
            + '/ Skewness = ' + str(np.round(self.skew,round_digits))\
            + '/ Kurtosis = ' + str(np.round(self.kurt,round_digits))\
            + '/ Sharpe = ' + str(np.round(self.sharpe,round_digits))\
            + '/ Median = ' + str(np.round(self.median,round_digits)) + '\n'\
            + '/ VaR 95% = ' + str(np.round(self.VaR_95,round_digits))\
            + '/ CVaR 95% = ' + str(np.round(self.CVaR_95,round_digits))\
            + '/ test Jarque-Bera = ' + str(np.round(self.jarque_bera,round_digits))\
            + '/ p_value = ' +str(np.round(self.p_value,round_digits))\
            + '/ Is normal: ' + str(self.is_normal)
        return plt_str

class capm_manager():
    
    def __init__(self,ric,bmk):
        self.nb_decimals = 4
        self.ric = ric
        self.bmk = bmk
        self.x = []
        self.y = []
        self.t = pd.DataFrame()
        self.beta = 0.0
        self.alpha = 0.0
        self.p_value = 0.0
        self.null_hypothesis = False
        self.r_value = 0.0
        self.r_squared = 0.0
        self.predictor_linreg = []
        
        
    def __str__(self):
        
       str_capm = 'Scatterplot of returns = ' + '\n'\
            + 'Linear regression / ric = ' + self.ric\
            + '/ Benchmark = ' + self.bmk + '\n'\
            + 'alpha (intercept) = ' + str(self.alpha)\
            + '/ beta (slope) = ' + str(self.beta) + '\n'\
            + 'p_value = ' + str(self.p_value)\
            + '/ null hypothesis = ' + str(self.null_hypothesis) + '\n'\
            + 'r_value = ' + str(self.r_value)\
            + '/ r_squared = ' + str(self.r_squared)
            
       return str_capm       
    
    def load_timeseries(self):
        # Load and sinchronise timeseries
        self.x, self.y, self.t = sf.sinchronise_timeseries(self.ric,self.bmk)
    
    def compute(self):        

        beta, alpha, r_value, p_value, std_err = linregress(self.x,self.y)
        self.beta = np.round(beta, self.nb_decimals)
        self.alpha = np.round(alpha, self.nb_decimals)
        self.p_value = np.round(p_value, self.nb_decimals)
        self.null_hypothesis = p_value > 0.05
        self.r_value = np.round(r_value, self.nb_decimals)
        self.r_squared = np.round(r_value**2, self.nb_decimals)
        self.predictor_linreg = alpha + self.beta*self.x
                      
    def scatterplot(self):        
      # Scatterplot of returns
        if self.beta > 0:
            color_beta = 'green'
        else:
            color_beta = 'red'        
            
        str_title = 'Scatterplot of returns' + '\n' + self.__str__()
        plt.figure()
        plt.title(str_title)
        plt.scatter(self.x,self.y)
        plt.plot(self.x,self.predictor_linreg, color = color_beta)
        plt.ylabel(self.ric)
        plt.xlabel(self.bmk)
        plt.grid()
        plt.show
        
        return str_title
        
    def plot_normailized(self):
        # Plot two timeseries normalized at 100
        ric = self.ric
        bmk = self.bmk
        # timestamps = self.t['date']
        price_ric = self.t[str(ric+' close')]
        price_bmk = self.t[str(bmk+' close')]
        plt.figure(figsize=(12,5))
        plt.title('Timeseries of prices | Normalized at 100')
        plt.ylabel(str(self.ric) + ' ' + str(self.bmk) + ' Normalized')
        plt.xlabel('Time')        
        price_ric = 100 * price_ric/price_ric[0]
        price_bmk = 100 * price_bmk/price_bmk[0]
        plt.plot(price_ric,color='blue',label=self.ric)
        plt.plot(price_bmk,color='red',label=self.bmk)
        plt.legend(loc=0)
        plt.grid()
        plt.show
    
    def plot_dual_axes(self):
        #Plot two timeseries with two vertical axes
        ric = self.ric
        bmk = self.bmk
        plt.figure(figsize=(12,5))
        plt.title('Timeseries of prices')
        plt.ylabel('Prices')
        plt.xlabel('Time')  
        # ax = plt.gca()
        ax1 = self.t[str(ric+' close')].plot(color = 'blue', grid=True, label=self.ric)
        ax2 = self.t[str(bmk+' close')].plot(color = 'red', grid=True, secondary_y=True, label=self.bmk)
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        plt.show
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
