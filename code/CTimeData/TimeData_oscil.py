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


""" Volatility Shit """
def get_ATR(self):
    """ ATR s an indicator that shows volatility of the market
    True Range is the greatest of the following three values:
            1- difference between the current maximum and minimum (high and low);
            2- difference between the previous closing price and the current maximum;
            3- difference between the previous closing price and the current minimum.
        It just wants to obtain the maximum range
    """

    """ Average True Range for volatility """
    rangeOC = self.get_timeSeries(["RangeCO"])
    magicDelta = self.get_timeSeries(["magicDelta"])
    diffPrevCloseCurrMin = self.get_diffPrevCloseCurrMin()
    diffPrevCloseCurrMax = self.get_diffPrevCloseCurrMax()
    
    print rangeOC.shape, magicDelta.shape, diffPrevCloseCurrMin.shape, diffPrevCloseCurrMax.shape
#    print dailyDelta.shape, magicDelta.shape, diffPrevCloseCurrMin.shape,diffPrevCloseCurrMax.shape
    All_diff = np.concatenate((rangeOC,magicDelta,diffPrevCloseCurrMin,diffPrevCloseCurrMax), axis = 1)
    All_diff = np.abs(All_diff)
    
    ATR = np.max(All_diff, axis = 1)
    
    return ATR

def get_MACD(self, Ls = 12, Ll = 26, Lsmoth = 9, alpha = -1):
    """ 
    Moving Average Convergence/Divergence (MACD) indicates the correlation between 
    two price moving averages.
    
    Usually 26-period and 12-period Exponential Moving Average (EMA).
    In order to clearly show buy/sell opportunities, 
    a so-called signal line (9-period indicators` moving average) is plotted on the MACD chart.
    The MACD proves most effective in wide-swinging trading markets. 
    There are three popular ways to use the Moving Average Convergence/Divergence: 
    crossovers, overbought/oversold conditions, and divergences.

    The MACD is calculated by subtracting the value of a 26-period exponential 
    moving average from a 12-period exponential moving average. 
    A 9-period dotted simple moving average of the MACD (the signal line) 
    is then plotted on top of the MACD.
    """
    
    MACD = indl.get_MACD(self.get_timeSeries(),Ls, Ll, Lsmoth,alpha)
    return MACD
    
def get_momentum(self, N = 1):
    """ 
    The Momentum Technical Indicator measures the amount that a 
    security’s price has changed over a given time span. 
    It is used with the closed price
    """
    
    momentum = indl.get_momentum(self.get_timeSeries(["Close"]), N)
    return momentum

def get_RSI(self, N = 1):
    """ 
    Relative Strength Index
    """
    
    momentum = indl.get_momentum(self.get_timeSeries(["Close"]), N)
    return momentum


def get_stochasticOscillator(self, N = 1):
    """ 
    Relative Strength Index
    """
    
    momentum = indl.get_momentum(self.get_timeSeries(["Close"]), N)
    return momentum


    