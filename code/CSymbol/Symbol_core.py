# -*- coding: utf-8 -*-
#import matplotlib

import numpy as np

import time
import pandas as pd
import graph_lib as gr
import Intraday_lib as itd
import utilities_lib as ul
import indicators_lib as indl
import get_data_lib as gdl 

import datetime as dt
from datetime import datetime

"""
Library with all the obtaining indicator functions of the market.

"""

# Start Date is the date from which we return the data.
# The data returned should be returned after this date.

# TimeSeries is the main data we have to care about. 
# All the operations will be done over this one

def get_currentPrice (self):
    # This function gets the current price from the lowest source
    minimumTimeScale = np.min(self.periods)
    currentPrice = self.TDs[minimumTimeScale].TD["Close"][-1]
    return currentPrice

def get_priceDatetime (self, datetime_ask, period):
    # This function gets the price for the given date in the given timeScale
    minimumTimeScale = np.min(self.periods)
    dates = self.TDs[period].TD.index
#    print datetime_ask
    good_dates = dates[dates == datetime_ask]
    good_prices = self.TDs[period].TD[dates == datetime_ask]["Close"]
    
#    print good_prices
    return good_prices[-1]



""" EXTENDED FUNCTIONS APPLIED TO ALL TIMESLOTS IN THE SYMBOL """

def set_interval(self,start_time = [], end_time = []):
    
    for period in self.periods:  # For each available period
        self.TDs[period].set_interval(start_time, end_time)
        
        
        