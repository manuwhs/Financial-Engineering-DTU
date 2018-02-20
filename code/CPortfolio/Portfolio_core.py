# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 03:04:26 2016

@author: montoya
"""


import numpy as np
import datetime as dt
import CSymbol as CSy


# secutities will be a dictionary of [symbol]
def set_symbols(self, symbols_list):
    # Sets the secutities list

    self.symbols = [] # Create the list of symbols
    for symbol_i in symbols_list:
        self.symbols[symbol_i.symbol] = symbol_i
    
    self.symbol_names = self.symbols.keys()
    self.Nsym = len(self.symbol_names) # Number of symbols

def set_symbols_names(self, symbols_names):
    # Sets the secutities list
    self.symbol_names = symbols_names
    self.Nsym = len(symbols_names)
def set_periods (self, periods):
    self.periods = periods;
    
def init_symbols(self, symbols_names = [], periods = []):
    # Sets the secutities list
    self.symbols = dict()
    if (symbols_names != []):
        self.set_symbols_names(symbols_names)
    
    if (periods != []):
        self.set_periods(periods)
        
    for symbol_i in self.symbol_names:
        self.symbols[symbol_i] = CSy.CSymbol(symbol_i,self.periods)
    
    
def set_intraRange (self,start_date, end_date):
    # Sets the start day and end day of the intraDay Study
    
    self.sd_dt = np.datetime64(start_date)
    self.ed_dt = np.datetime64(end_date)
    
def set_dailyRange (self,start_date, end_date):
    # Sets the start day and end day of the study.
    # To do so, we just modify self.dailyData to be in that range.
    # The problem is that moving averages and shit needs earlier info so...
    self.si_dt = dt.datetime(start_date)
    self.ei_dt = dt.datetime(end_date)

def set_interval(self,start_time = [], end_time = []):
    for symbol_n in self.symbol_names:
        self.symbols[symbol_n].set_interval(start_time, end_time)

def get_dates(self, symbol, period):
    # This function gets the dates of one of the symbols
    # and one of the intervals
    return self.symbols[symbol].TDs[period].get_dates()

def get_Returns(self, period):
    ## This function gets the returns for the period given
    i = 0
    for symbol_n in self.symbol_names:
#        print symbol_n
        ret_aux = self.symbols[symbol_n].TDs[period].get_timeSeriesReturn();
#        print ret_aux.shape
        if (i == 0):
            ret = ret_aux
            i = i +1
        elif (i > 0):
            ret = np.concatenate((ret,ret_aux),axis = 1)
    
    return ret
    
def get_timeSeries(self, period):
    ## This function gets the returns for the period given
    i = 0
    for symbol_n in self.symbol_names:
        ret_aux = self.symbols[symbol_n].TDs[period].get_timeSeries();
        if (i == 0):
            ret = ret_aux
            i = i +1
        elif (i > 0):
            ret = np.concatenate((ret,ret_aux),axis = 1)
                        
#        print i
#        print ret.shape
        
#    print "Concat"
#    print ret.shape
    return ret
    
def get_CumReturns(self,period):
    # Concatenate several [Nsamples][1] Series
    
    i = 0
    for symbol_n in self.symbol_names:
        ret_aux = self.symbols[symbol_n].TDs[period].get_timeSeriesCumReturn();
        if (i == 0):
            ret = ret_aux
        elif (i > 0):
            ret = np.concatenate((ret,ret_aux),axis = 1)
        i = i +1
    return ret

def get_dailyReturns(self):
    # Concatenate several [Nsamples][1] Series
    ret = self.get_Returns(period = 1440)
    return ret
    
def get_dailyCumReturns(self):
    # Concatenate several [Nsamples][1] Series
    ret = self.get_CumReturns(period = 1440)
    return ret
