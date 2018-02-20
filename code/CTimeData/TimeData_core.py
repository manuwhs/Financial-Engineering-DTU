# -*- coding: utf-8 -*-
#import matplotlib

###### IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
## Si devolvemos algun self.XXXX, devolver un copy.deepcopy()
import numpy as np
import copy
import time
import pandas as pd
import graph_lib as gr
import Intraday_lib as itd
import utilities_lib as ul
import indicators_lib as indl
import get_data_lib as gdl 
import basicMathlib as bMl

import datetime as dt
from datetime import datetime

"""
Library with all the obtaining indicator functions of the market.

"""

# Start Date is the date from which we return the data.
# The data returned should be returned after this date.

# TimeSeries is the main data we have to care about. 
# All the operations will be done over this one

def set_period (self, period):
    # Sets the period date in minuts
    self.period = period 
    
def get_period (self):
    return copy.deepcopy(self.period);

def set_seriesNames(self, seriesNames = []):
    if (seriesNames == []):
        seriesNames = ["Close"]
        
    self.seriesNames = seriesNames;
    self.timeSeries = [];
    
def get_seriesNames(self):
    return copy.deepcopy(self.seriesNames);

def set_interval(self,start_time = [], end_time = []):
    
    if (len(self.TD) != 0):   # If the csv is not empty we fill it with the max
        if (start_time == []):
            self.start_time = self.TD.index[0]
        if (end_time == []):
            self.end_time = self.TD.index[-1]  
            
        if (start_time != []):
            self.start_time = start_time
        if (end_time != []):
            self.end_time = end_time
        
        ## If both start and end are set we then calculate the mask !!!
        if ((self.start_time != [])& (self.end_time != [])):
            dates = self.TD.index
            self.time_mask = (dates >= self.start_time) & (dates <= self.end_time)
            
#            print len(dates)
#            print len(self.time_mask)

def get_timeSeries(self, seriesNames = [], transform = "log"):
    # The final timeSeries will be [Nsamples][Nsec]
    # TODO  : Make it possible to add other names that will be a funciton of the original prices
    
    transform = "pene"
    if (seriesNames != []):   # If we indicate a new type of seriesNames
        self.set_seriesNames(seriesNames)
    
    timeSeries = []
    for name in self.seriesNames:
        if (name == "Average"):
            timeSeries.append(np.mean(self.TD[["Low","High","Close","Open"]], axis = 1))
        
        elif(name == "RangeHL"):  # Difference Between High and Low
            Range = np.array(self.TD["High"][:] - self.TD["Low"][:])
            timeSeries.append(Range)
            
        elif(name == "RangeCO"):  # Difference between Close and Open
            Range = self.TD["Close"][:] - self.TD["Open"][:]
            timeSeries.append(Range)
            
        elif(name == "magicDelta"):  # Difference between Close and Open
            magicDelta = self.get_magicDelta()
            timeSeries.append(magicDelta)
            
        else:
            timeSeries.append(self.TD[name])
            
    timeSeries = np.array(timeSeries).T;  # timeSeries[Nvalues][Ntimes]
    dates = self.TD.index

#    print timeSeries.shape
    self.timeSeries = timeSeries[self.time_mask,:]    # Price List we are operating with timeSeries[Nvalues][Ndates]
    # TODO if we convert dates to np.array it converts dt.datetime to np.datetime64
    self.dates = dates[self.time_mask]              # Dates we are operating with 
#    print timeSeries.shape
    if (transform == "log"):
        self.timeSeries = np.log(self.timeSeries)
        
    return copy.deepcopy(self.timeSeries)

def get_dates(self):
    # Gets the dates vector, if we dont have it, we create it
#    if (len(self.dates) == 0):  # Check existence of timeSeries
    dates = self.TD.index[self.time_mask]
    self.dates = dates
    return copy.deepcopy(self.dates)


def get_timeSeriesReturn(self, transform = "log"):
    # Gets the Return of the Time Series, if it has not been created yet, then it creates it
    # if (self.timeSeries == []):  # Check existence of timeSeries
    transform = "pene"
    # We will try as well to get the return of the first datapoint
    # if we actually have it in the database. For this, we check our mask.
    # If the first "1" found is not at 0, we can do this
    
    self.get_timeSeries(transform = "tus muertos")
    
    pos1 = (self.time_mask).tolist().index(1)

    if (pos1 > 0): # If we actually have more signal.
        ps = self.TD[self.seriesNames].iloc[pos1-1]
        ps = np.array(ps).T
        ps = ps.reshape(ps.size/len(self.seriesNames), len(self.seriesNames))
#        print ps
#        print self.timeSeries.shape
#        print ps.shape
        self.timeSeriesReturn = bMl.get_return(np.concatenate((ps,self.timeSeries),axis =0))
        self.timeSeriesReturn = self.timeSeriesReturn[1:,:]
    else:
        self.timeSeriesReturn = bMl.get_return(self.timeSeries)
    
    if (transform == "log"):
    ## We perform log of this shit + 1 to get the log returns
        self.timeSeriesReturn = np.log(self.timeSeriesReturn + 1)
    
    return copy.deepcopy(self.timeSeriesReturn)

def get_timeSeriesCumReturn(self):
    # Gets the Return of the Time Series, if it has not been created yet, then it creates it
    #if (self.timeSeries == []):  # Check existence of timeSeries
    self.get_timeSeries()
        
    self.timeSeriesCumReturn = bMl.get_cumReturn(self.timeSeries)
    return copy.deepcopy(self.timeSeriesCumReturn)

# The rest of functions supose that the timeSeries has been created.
#### GET ONLY DAILY SHIT

def get_SortinoR(self):
    # if (self.timeSeriesReturn == []):
    self.get_timeSeriesReturn();
        
    SortinoR = ul.get_SortinoR(self.timeSeriesReturn)
    
    return SortinoR;
    
def get_SharpR(self):
    # if (self.timeSeriesReturn == []):
    self.get_timeSeriesReturn();
        
    self.get_SharpR = ul.get_SharpR(self.timeSeriesReturn)
    return copy.deepcopy(self.get_SharpR)
    
##################################################################
######################   DIFERENCES DATA    ######################
##################################################################
"""  Here we define other time series obtained from linear operations
over the basic ones"""

def get_magicDelta(self):
    # Difference between the open of one day and the close of the preceiding day
    closePrev = self.TD["Close"].values
    openCurr = self.TD["Open"].values

    magicDelta = np.array(openCurr[1:] - closePrev[:-1])
    magicDelta = np.concatenate(([0],magicDelta), axis = 0)
#    print magicDelta
#    print len(openCurr[1:])
#    print (magicDelta.shape)
    
    return magicDelta

def get_diffPrevCloseCurrMax(self):
    
    # Difference between the open of one day and the close of the preceiding day
    PrevClose = self.TD["Close"].values
    CurrMax = self.TD["High"].values

    diffPrevCloseCurrMax = np.array(PrevClose[1:] - CurrMax[:-1]).reshape((len(PrevClose)-1,1))
    zero_vec = np.zeros((1,1))  # Add zero vector
    diffPrevCloseCurrMax = np.concatenate((zero_vec,diffPrevCloseCurrMax), axis = 0)
    
    return copy.deepcopy(diffPrevCloseCurrMax[self.time_mask,:])

def get_diffPrevCloseCurrMin(self):
    
    # Difference between the open of one day and the close of the preceiding day
    PrevClose = self.TD["Close"].values
    CurrMin = self.TD["Low"].values

#    print len(PrevClose)
    diffPrevCloseCurrMin = np.array(PrevClose[1:] - CurrMin[:-1]).reshape((len(PrevClose)-1,1))
    zero_vec = np.zeros((1,1))  # Add zero vector
#    print diffPrevCloseCurrMin.shape
    diffPrevCloseCurrMin = np.concatenate((zero_vec,diffPrevCloseCurrMin), axis = 0)
    
    return copy.deepcopy(diffPrevCloseCurrMin[self.time_mask,:])
    
#### GET the time series divided in days #####
def get_intra_by_days(self):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
        
    days_list_price = [];
    days_list_dates = [];
    
    price = self.timeSeries
    dates = self.dates

#        print type(dates[0])
    days_dates = ul.get_dates(dates)
    diff_days = np.unique(days_dates)
    
    for day_i in range (len(diff_days)):
        
        day_intra_indx = (days_dates == diff_days[day_i])
        day_intra_price = price[day_intra_indx,:]
        day_intra_date = dates[day_intra_indx]
        
        days_list_price.append(day_intra_price)
        days_list_dates.append(day_intra_date)
        
    return days_list_price, days_list_dates
    
