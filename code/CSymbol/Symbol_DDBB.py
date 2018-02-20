# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from numpy import loadtxt

import time
import pandas as pd
import graph_lib as gr
import Intraday_lib as itd
import utilities_lib as ul
import indicators_lib as indl
import get_data_lib as gdl 

import datetime as dt
import CTimeData as CTD

#############################################################
################# BASIC FUNCTIONS FOR A GIVEN PERIOD ########
############################################################

def set_periods (self, periods):
    self.periods = periods;

def init_timeDatas(self):
    # Initialize the Periods
    for period in self.periods:  # Creates emppty Dataframes
        self.TDs[period] = CTD.CTimeData(self.symbol, period, ul.empty_df);

def set_timeDataPeriod (self, timeData, period):
    # Set period
    self.TDs[period] = CTD.CTimeData(self.symbol, period,timeData);

def get_timeDataPeriod (self, period = 1440):
    return self.TDs[period].TD

def add_timeDataPeriod(self, new_TimeData, period = 1440):

    self.TDs[period].TD = new_TimeData.combine_first(self.TDs[period].TD) 

def load_csv_timeData_period(self, file_dir = "./storage/", period = 1440):
    # The file must have the name:
    #  symbolName_TimeScale.csv
    whole_path = file_dir + self.symbol + "_" + ul.period_dic[period] + ".csv"
    try:
        dataCSV = pd.read_csv(file_dir + self.symbol + "_" + ul.period_dic[period] + ".csv",
                              sep = ',', index_col = 0, dtype = {"Date":dt.datetime})
        
        dataCSV.index = dataCSV.index.astype(dt.datetime)   # We transform the index to the real ones
        
    except IOError:
        error_msg = "File does not exist: " + whole_path 
        print error_msg
        dataCSV = ul.empty_df
        
    return dataCSV

#############################################################
################# BASIC FUNCTIONS FOR ALL PERIODS  ########
############################################################

def set_csv(self,file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    for period in self.periods:
#        print period
        self.TDs[period].set_csv(file_dir)
    
def add_csv(self,file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    for period in self.periods:
        self.TDs[period].add_csv(file_dir)

def save_to_csv(self,file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    for period in self.periods:
#        print period
        self.TDs[period].save_to_csv(file_dir)

## Loads all the TDS of the symbol from yahoo
def download_TDs_yahoo(self,sdate,edate,file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    for period in self.periods:
#        print period
        self.TDs[period].download_from_yahoo(sdate,edate)

## Loads all the TDS of the symbol from yahoo and updates them
def update_TDs_yahoo(self,sdate,edate,file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
     self.download_TDs_yahoo(sdate,edate)
     self.add_csv(file_dir)  ## Add it to the one we already have
     self.save_to_csv(file_dir)

#######################################################################
############## Complex Func  ##########################################
#######################################################################

def update_TDs (self,file_dir_current = "./storage/", file_dir_new = "../Trader/MQL4/Files/" ):
    self.set_csv(file_dir_current)
    self.add_csv(file_dir_new)
    self.save_to_csv(file_dir_current)

