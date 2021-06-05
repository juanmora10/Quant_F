# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 02:01:50 2021

@author: eljua
"""
# Importar librerias

# import numpy as np
# import pandas as pd
# import matplotlib as mpl
# import scipy
import importlib
# import matplotlib.pyplot as plt
# from scipy.stats import skew, kurtosis, chi2
# from scipy.optimize import minimize
# from numpy import linalg as LA

# Import own files
import stream_functions as sf
importlib.reload(sf)
import stream_clases as sc
importlib.reload(sc)

# Determinar ticker
ric = 'MXN=X' # ^VIX MXN=X ^IXIC DBK.DE  # file_extension = '.csv'

# uso de la función 'load_ts'
x, title, t = sf.load_ts(ric)
sf.plot_ts(t,ric,title)

# Test de Jarque Bera
jb = sc.jarque_bera_test(ric)
jb.load_timeseries()
jb.compute()

print(jb)

# graficar histograma


