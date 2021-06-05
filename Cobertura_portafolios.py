# -*- coding: utf-8 -*-
"""
Created on Wed May  5 17:55:05 2021

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
# Import own files
import stream_functions as sf
importlib.reload(sf)
import stream_clases as sc
importlib.reload(sc)

ric = '^VIX'

jb = sc.jarque_bera_test(ric)
jb.load_timeseries()
jb.compute()
jb.plt_str()
sf.plot_hist()
