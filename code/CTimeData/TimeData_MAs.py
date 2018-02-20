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
Library with all Moving Averages

"""
"""" MOVING AVERAGES """ 
def get_SMA(self, L ):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    SMA = indl.get_SMA(self.timeSeries, L)
    
    return SMA

def get_WMA(self, L ):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    WMA = indl.get_WMA(self.timeSeries, L)
    
    return WMA
    
def get_EMA(self, L, alpha = -1):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    EMA = indl.get_EMA(self.timeSeries, L, alpha)
    
    return EMA

def get_MAg(self, L, alpha = -1):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    EMA = indl.get_Mag(self.timeSeries, L, alpha)
    
    return EMA
    
def get_HMA(self, L):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    HMA = indl.get_HMA(self.timeSeries, L)
    
    return HMA
    
def get_TrCrMr(self, alpha = -1):
    if (self.timeSeries == []):  # Check existence of timeSeries
        self.get_timeSeries()
    get_TrCrMr = indl.get_TrCrMr(self.timeSeries, alpha)
    
    return get_TrCrMr



    

    
    