# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import utilities_lib as ul
import get_data_lib as gdl 
import datetime as dt
import DDBB_lib as DBl  # For getting data

""" LIBRARY FOR OPERATION RELATED TO THE BBDD of the marcket """
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

Where Date is the index and is in numpy.datetime64.
A set of functions for dealing with it will be specified. 
Set of functions such as add values, delete values will be done.

"""

#############################################################
################# BASIC FUNCTIONS ##########################
############################################################

def set_timeData (self, timeData): # Stablish the initial data
    self.TD = timeData;
    self.set_interval()  # Set the interval to the maximum possible
    
    ### TODO this dos the sorting, check when is it best to do so
    self.TD.sort_index(inplace=True)
    
def get_timeData (self):
    return self.TD

def add_timeData(self, new_TimeData):
    # This function adds new data to the existing Daily data 
    # It places it into the positions refered by the "Index" date.
    # If there are days with the same index, they get overwritten.
    # new_dailyData is expected to have nice format

#        self.dailyData = pd.concat([self.dailyData, new_dailyData], verify_integrity = True)
#        self.dailyData = pd.merge(self.dailyData, new_dailyData)
    # Combine both pandas overwitting the old with the new
    self.TD = new_TimeData.combine_first(self.TD) 
    self.TD.sort_index(ascending = False)
    self.set_timeData(self.TD)   # To make the interval
    
def save_to_csv(self, file_dir = "./storage/"):
    ul.create_folder_if_needed(file_dir)
    whole_path = file_dir + ul.period_dic[self.period] + "/" + self.symbol + "_" + ul.period_dic[self.period] + ".csv"
    ul.create_folder_if_needed(file_dir + ul.period_dic[self.period] + "/")
    self.TD.to_csv(whole_path, sep=',')

def load_csv_timeData(self, file_dir = "./storage/"):
    # The file must have the name:
    #  symbolName_TimeScale.csv
    # TODO put periods in loading
    whole_path = file_dir + ul.period_dic[self.period] + "/" + self.symbol + "_" + ul.period_dic[self.period] + ".csv"
    try:
        dataCSV = pd.read_csv(whole_path,
                          sep = ',', index_col = 0, dtype = {"Date":dt.datetime})
    
        dataCSV.index = ul.str_to_datetime (dataCSV.index.tolist())
        
    except IOError:
        error_msg = "File does not exist: " + whole_path 
        print error_msg
        dataCSV = ul.empty_df
    
    except:
        print "Unexpected error in file: " + whole_path
    # We transform the index to the real ones

    return dataCSV
    
#######################################################################
############## Set and Add from csvs ###################################
#######################################################################

def set_csv(self, file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    newCsv = self.load_csv_timeData(file_dir)
    self.set_timeData(newCsv)
    
def add_csv(self, file_dir = "./storage/"):
    # Loads a CSV and adds its values to the main structure
    newCsv = self.load_csv_timeData(file_dir)
    self.add_timeData(newCsv)

def update_csv (self,file_dir_current = "./storage/", file_dir_new = "../Trader/MQL4/Files/" ):
    self.set_csv(file_dir_current)
    self.add_csv(file_dir_new)
    self.save_to_csv(file_dir_current)
    
# Update the current data using yahoo
def download_from_yahoo(self,start_date = "01-12-2011", end_date = "01-12-2015" ):
    
    precision = "1mo"
    dataCSV = DBl.get_data_yahoo(self.symbol, precision, 
                   start_date , end_date)
                   
    self.set_timeData(dataCSV)
    return dataCSV
    
def update_csv_yahoo (self,sdate,edate,file_dir_current = "./storage/"):
    self.download_from_yahoo(sdate,edate)
    self.add_csv(file_dir_current)  ## Add it to the one we already have
    self.save_to_csv(file_dir_current)


#######################################################################
############## Add from the Internet ###################################
#######################################################################
 
def addDaily_from_google (self,start_date, end_date):
    data_daily_google = gdl.get_dayly_google(self.symbol,start_date, end_date )
    
    self.add_DailyData(data_daily_google)

def addDaily_from_yahoo (self,start_date, end_date):
    data_daily_google = gdl.get_dayly_yahoo(self.symbol,start_date, end_date )
    
    self.add_DailyData(data_daily_google)
    
def addIntra_from_google (self,days_back):
    # Days_back is the number of days back we get the data.
    # It cannot exeed 14 for google
    data_intra_google = gdl.get_intra_google(self.symbol, self.period * 60, days_back)
    
    self.add_IntraData(data_intra_google)

def addIntra_from_yahoo (self,days_back):
    # Days_back is the number of days back we get the data.
    # It cannot exeed 14 for google
    data_intra_google = gdl.get_intra_yahoo(self.symbol, self.period * 60, days_back)
    
    self.add_IntraData(data_intra_google)


  
######################################################################
############## BBDD data processing ###################################
#######################################################################
 
def check_data(self):  # TODO
    # Check that there are no blanck data or wrong
    print "checking"
    
def data_filler(self): # In case we lack some data values
    # We can just fill them with interpolation
    # We do this at csv level 

    self.dailyData 
    start_date = self.dailyData.index[0].strftime("%Y-%m-%d")   #strptime("%Y-%m-%d")
    end_date = dt.datetime(self.dailyData.index[-1].strftime("%Y-%m-%d"))
    
    print start_date
    # We have to get all working days between these 2 dates and check if
    # they exist, if they dont, we fill them
    # Create days of bussines
    
    busday_list = []
    
    next_busday = np.busday_offset(start_date, 1, roll='forward')
    busday_list.append(next_busday)
    
    while (next_busday < end_date): # While we havent finished
#        print next_busday, end_date
        next_busday = np.busday_offset(next_busday, 1, roll='forward')
        busday_list.append(next_busday)

    Ndays_list = len(busday_list)   # Number of days that there should be
    Ndays_DDBB = len(self.dailyData.index.tolist())
    
    print Ndays_list, Ndays_DDBB  ## TODO
    
    
#    for i in range (Ndays_list):
#        print "e"
        
    print start_date, end_date

