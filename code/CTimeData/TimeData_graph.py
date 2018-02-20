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

from graph_lib import gl
######################################################################
############# BASIC PLOTS #######################################
######################################################################
    
def plot_timeSeries(self, nf = 1, na = 0):
    dates = self.dates
    timeSeries = self.get_timeSeries()

    gl.plot(dates, timeSeries, nf = nf,
            labels = [self.symbol + "(" + str(self.period) + ")", 
            "Time (" + str(self.period) + ")", "Prices"],
            legend = self.seriesNames, na = na)

def plot_timeSeriesReturn(self, nf = 1):
    dates = self.dates
    timeSeries = self.get_timeSeriesReturn()
    
    gl.plot(dates, timeSeries, nf = nf,
            labels = [self.symbol + "(" + str(self.period) + ")", 
            "Time (" + str(self.period) + ")", "Return Prices"],
            legend = self.seriesNames, fill = 1)

def plot_timeSeriesCumReturn(self, nf = 1):
    dates = self.dates
    timeSeries = self.get_timeSeriesCumReturn()
    
    gl.plot(dates, timeSeries, nf = nf,
            labels = [self.symbol + "(" + str(self.period) + ")", 
            "Time (" + str(self.period) + ")", "CumReturn Prices"],
            legend = self.seriesNames)

######################################################################
############# BASIC Veleros #######################################
######################################################################

def plot_dailyVJ(self):
    ## PLOTS DAILY Velas Japonesas

    data = np.matrix(self.TD[['Close', 'Open', 'High', 'Low']][self.time_mask].values).T
    volume = self.TD['Volume'][self.time_mask].values
#    print data
    labels = ["Velas Japonesas","Day","Price",self.symbol]
    gr.Velero_graph([], data, volume, labels,new_fig = 1)
    
def plot_dailyHA(self):
    ## PLOTS DAILY HEIKE ASHI

    data = self.TD[['Open', 'High', 'Low', 'Close']].iloc[self.time_mask]
    volume = self.TD['Volume'].values[self.time_mask]

    labels = ["Heiken Ashi","Day","Price",self.symbol]
    gr.Heiken_Ashi_graph([], data, volume, labels,new_fig = 1)

def plot_trendVJ(self):
    ## PLOTS DAILY Velas Japonesas pero sólo teniendo en cuenta los Max y min

    data = np.matrix(self.TD[['High', 'Low']][self.time_mask].values).T
    volume = self.TD['Volume'][self.time_mask].values
#    print data
    labels = ["Velas Japonesas","Day","Price",self.symbol]
    gr.TrendVelero_graph([], data, volume, labels,new_fig = 1)
    
######################################################################
############# Specific Graphs #######################################
######################################################################
    
def scatter_deltaDailyMagic(self):
    ## PLOTS DAILY HEIKE ASHI
    ddelta = self.get_dailyDelta()
    mdelta = self.get_magicDelta()
    labels = ["Delta Magic Scatter","Magic","Delta",self.symbol]
    gr.scatter_graph(mdelta,ddelta, labels,new_fig = 1)
    

######################################################################
############# Moving Averages Graph #######################################
######################################################################

def plot_TrCrMr(self):
    ## PLOTS DAILY HEIKE ASHI
    self.get_timeSeries()
    TrCrMr = self.get_TrCrMr()
    labels = ["Delta Magic Scatter","Magic","Delta",self.symbol]
    gr.plot_graph([],self.timeSeries, labels,new_fig = 1)
    
    labels = ["Delta Magic Scatter","Magic","Delta",["Real","Mieeda","d","fr"]]
    gr.plot_graph([],TrCrMr, labels,new_fig = 0)

def plot_MA(self, flags):
    """ Function that plots the price and the indicated Moving Averages """
    
    self.get_timeSeries()

    labels = ["Delta Magic Scatter","Magic","Delta",self.symbol]
    gr.plot_graph([],self.timeSeries.T, labels,new_fig = 1)
    
    if (flags == 5):
        HMA = self.get_HMA(200)
        labels = ["Delta Magic Scatter","Magic","Delta",self.symbol]
        gr.plot_graph([],HMA, labels,new_fig = 0)
        
    if (flags == 3):
        ATR = self.get_ATR()
        print ATR.shape, self.timeSeries.shape
        labels = ["Delta Magic Scatter","Magic","Delta"]
        gr.plot_graph([], np.matrix(self.timeSeries).T + ATR.T, labels,new_fig = 0)

        

def plot_BollingerBands(self, new_figure = 0, L = 21):
    if (new_figure == 1):
        self.new_plot(title = "Bollinger Bands", xlabel = "time", ylabel = "Close")
    
    SMA = self.get_SMA(L = L)
    BB = self.get_BollingerBand(L = L)
    
    self.plot_timeSeries()
    self.add_plot_graph([],SMA + BB, ["SMA + BB"])
    self.add_plot_graph([],SMA - BB, ["SMA - BB"])

######################################################################
############# ELABORATE PLOTS #######################################
######################################################################
        
def plot_TD(self,start_date = [], end_date = []):
    
    labels = ['Close value', "Days", 'Adjusted Close']
    
    ### GET THE SUBSELECTION OF DAYS DATA ###
    if (start_date != []) and (end_date != []):  # If we specify a date
    
        start_date = dt.datetime(start_date).astype(datetime)
        end_date = dt.datetime(end_date).astype(datetime)
 
        index_time_list = self.TD.index.date  # Obtain the date only
#            print index_time_list
        
        indexs = np.where( index_time_list < end_date) and np.where( index_time_list > start_date)
        
#            print indexs
        
        # Subselection of the indexes 
        Close = self.intraData.ix[indexs]["Close"].values
        
    else:
        Close = self.intraData["Close"].values
        
    gr.plot_graph([],Close.T,labels, 1)
