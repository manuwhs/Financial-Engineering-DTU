# -*- coding: utf-8 -*-


import pandas as pd
import utilities_lib as ul
#### IMPORT the methods
import TimeData_core as TDc    # Core methods
import TimeData_MAs as TDMAs   # Moving Averages 
import TimeData_oscil as TDos   # Ocillators
import TimeData_volat as TDvo  # Volatility
import TimeData_graph as TDgr   # Graphics
import TimeData_DDBB as TDDB   # Graphics
import TimeData_intors as intr

""" A container to store prices for a symbol:
This Class will contain for a given symbol:
  - Daily Data.
  - Intraday Data.
  
Functions to:
- Load data into it from any specific source 
- Store itself into Disk to be loaded afterwards
- """

""" Dayly data will be a pandas Dataframe with the structure:

              Open    High     Low   Close    Volume
Date                                               
2015-02-03  121.74  121.76  120.56  121.05   8255863
2015-02-04  121.63  122.22  120.92  121.58   5386747
2015-02-05  120.98  121.83  120.61  121.79   6879945
2015-02-06  119.15  119.52  117.95  118.64  13206906

Where Date is the index and is in dt.datetime.
A set of functions for dealing with it will be specified. 
Set of functions such as add values, delete values will be done.

"""

class CTimeData:
    
    def __init__(self, symbol = "None", period = -1, timeData = ul.empty_df):
        self.symbol = symbol    # Symbol of the Security (GLD, AAPL, IDX...)
        self.period = period
        
        ## Time constraining variables
        self.start_time = []  # Start and end of period to operate from the TD
        self.end_time = []
        self.mask_time =[]
        
        # There is a set of flags for precomputed shit that does not have to be precomputed again
        self.set_timeData(timeData)   # To make the interval
        # If timeData is empty initially then no interval will be set
        
        # Primary variables
        self.timeSeries = [];
        self.dates = []
        self.set_seriesNames()   # Names of the signals we are working with ("Open", "Low", "Average", "Volume")
                                 # If indicated with a new function, then they change
        
        self.figure = -1;  
        self.labels = []; # Array of labels to have in a graph
        
        ## Secondary Variables
        self.timeSeriesReturn = []
        self.timeSeriesCumReturn = []
        
    #######################################################################
    ############## DDBB methods ###########################################
    #######################################################################
    set_csv = TDDB.set_csv    # Set and add timeData from csv's
    add_csv = TDDB.add_csv
    save_to_csv = TDDB.save_to_csv # Save timeData to csv
    
    update_csv = TDDB.add_csv
    download_from_yahoo = TDDB.download_from_yahoo
    update_csv_yahoo = TDDB.update_csv_yahoo
    
    # Intern functions
    set_timeData = TDDB.set_timeData
    get_timeData = TDDB.get_timeData
    add_timeData = TDDB.add_timeData
    load_csv_timeData = TDDB.load_csv_timeData
    
    #######################################################################
    ############## CORE Methods ###########################################
    #######################################################################
    
    set_period = TDc.set_period
    get_period = TDc.get_period
    set_seriesNames = TDc.set_seriesNames
    get_seriesNames = TDc.get_seriesNames
    

    set_interval = TDc.set_interval
    get_timeSeries = TDc.get_timeSeries
    get_dates = TDc.get_dates
    get_timeSeriesReturn = TDc.get_timeSeriesReturn
    get_timeSeriesCumReturn = TDc.get_timeSeriesCumReturn
    
    get_magicDelta = TDc.get_magicDelta
    get_diffPrevCloseCurrMin = TDc.get_diffPrevCloseCurrMin
    get_diffPrevCloseCurrMax = TDc.get_diffPrevCloseCurrMax
    
    get_SortinoR = TDc.get_SortinoR
    get_SharpR = TDc.get_SharpR
    
    get_intra_by_days = TDc.get_intra_by_days
    
    #######################################################################
    ############## Moving Averages  ###########################################
    #######################################################################
    
    get_SMA = TDMAs.get_SMA
    get_WMA = TDMAs.get_WMA
    get_EMA = TDMAs.get_EMA
    get_TrCrMr = TDMAs.get_TrCrMr

    get_HMA = TDMAs.get_HMA
    get_MAg = TDMAs.get_MAg
    
    #######################################################################
    ############## Indicators  ###########################################
    #######################################################################
    
    get_BollingerBand = intr.get_BollingerBand

    #######################################################################
    ############## Ocillators  ###########################################
    #######################################################################
    get_ATR = TDos.get_ATR
    get_MACD = TDos.get_MACD
    get_momentum = TDos.get_momentum
    get_RSI = TDos.get_RSI
    
    #######################################################################
    ############## Graphics  ###########################################
    #######################################################################

    plot_timeSeries = TDgr.plot_timeSeries
    plot_timeSeriesReturn = TDgr.plot_timeSeriesReturn
    plot_timeSeriesCumReturn = TDgr.plot_timeSeriesCumReturn
    
    plot_dailyHA = TDgr.plot_dailyHA
    plot_dailyVJ = TDgr.plot_dailyVJ
    plot_trendVJ = TDgr.plot_trendVJ
    
    scatter_deltaDailyMagic = TDgr.scatter_deltaDailyMagic
    plot_TrCrMr = TDgr.plot_TrCrMr
    plot_MA = TDgr.plot_MA
    
    plot_BollingerBands = TDgr.plot_BollingerBands
#pd.concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False,
#       keys=None, levels=None, names=None, verify_integrity=False)
       



