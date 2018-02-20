# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 03:04:26 2016

@author: montoya
"""

import pandas as pd
import numpy as np
import urllib2
import datetime as dt
import matplotlib.pyplot as plt
import copy as copy
import time as time

import pandas.io.data as web
import datetime
import gc
## Operations from a list of symbols 

def update_symbols_csv(self, file_dir_current = "./storage/", file_dir_new = "../Trader/MQL4/Files/"):
   for sym_i in self.symbol_names:   # Iterate over the securities
       symbol = self.symbols[sym_i]
       symbol.update_TDs(file_dir_current, file_dir_new)
       gc.collect()  # Remove the unreachable space
       
def load_symbols_csv(self, file_dir = "./storage/"):
    # Load symbols from disk
   for sym_i in self.symbol_names:   # Iterate over the securities
       symbol = self.symbols[sym_i]
       symbol.set_csv(file_dir)
       
def save_to_csv(self, file_dir = "./storage/"):
   for sym_i in range(self.symbol_names):   # Iterate over the securities
       symbol = self.symbols[sym_i]
       symbol.save_to_csv(file_dir)
       
### Download the symbols from Yahoo and update the ones we already have
def download_symbols_csv_yahoo(self, sdate,edate, file_dir_current = "./storage/"):
   for sym_i in self.symbol_names:   # Iterate over the securities
       symbol = self.symbols[sym_i]
       symbol.download_TDs_yahoo(sdate,edate,file_dir_current)
       gc.collect()  # Re

def update_symbols_csv_yahoo(self, sdate,edate, file_dir_current = "./storage/"):
   for sym_i in self.symbol_names:   # Iterate over the securities
       symbol = self.symbols[sym_i]
       symbol.update_TDs_yahoo(sdate,edate,file_dir_current)
       gc.collect()  # Remove the unreachable space
           
      