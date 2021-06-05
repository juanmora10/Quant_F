# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:29:12 2021

@author: eljua
"""

import importlib


# Import own files
import stream_functions as sf
importlib.reload(sf)
import stream_clases as sc
importlib.reload(sc)

ric = 'SGRE.MC' # ^VIX MXN=X ^IXIC DBK.DE  CL=F SGRE.MC
bmk = '^STOXX'  # ^STOXX

# sincrinise timeseries

# x, y, t = sf.sinchronise_timeseries(ric,bmk)

modelo = sc.capm_manager(ric,bmk)
modelo.load_timeseries()
modelo.compute()
modelo.scatterplot()
modelo.plot_normailized() # Two timeseries normalized
modelo.plot_dual_axes() # Dual axes
print(modelo)




