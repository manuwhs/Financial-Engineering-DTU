# -*- coding: utf-8 -*-
import pandas as pd

#### IMPORT the methods
import Symbol_core as Syc    # Core methods
import Symbol_DDBB as SyDB   # Graphics
import CTimeData as CTD

def load_symbol_info(file_dir = "./storage/"):
    # This functions loads the symbol info
    whole_path = file_dir + "Symbol_info.csv"
    try:
        infoCSV = pd.read_csv(whole_path,
                              sep = ',')
    except IOError:
        error_msg = "Empty file: " + whole_path 
        print error_msg
        
    return infoCSV
                             
class CSymbol:
    
    def __init__(self, symbol = "None", periods = []):
        self.symbol = symbol    # Symbol of the Security (GLD, AAPL, IDX...)
        self.periods = periods     # Periods for which we have TimeData
        self.TDs = dict()    # Dictionary   TimeDatas[period] = CTimeData for that period
        
        # Loop over the periods to get all the TimeDatas
        
        ## TODO define the variables that state the properties of the symbol
        self.open_time = [];   # Time at which it is open
        self.type = "Share"
        self.country = "Spain"
        self.currency = "EUR"
        self.sector = "Energy" 
        
        if (periods != []):
            self.init_timeDatas();  # Initialize TD dataframes to 0 and stablish their Symbol and period

    init_timeDatas = SyDB.init_timeDatas
    set_periods = SyDB.set_periods
    
    set_timeDataPeriod = SyDB.set_timeDataPeriod
    get_timeDataPeriod = SyDB.get_timeDataPeriod
    add_timeDataPeriod = SyDB.add_timeDataPeriod
    load_csv_timeData_period = SyDB.load_csv_timeData_period
    
    set_csv = SyDB.set_csv
    add_csv = SyDB.add_csv
    save_to_csv = SyDB.save_to_csv
    
    download_TDs_yahoo = SyDB.download_TDs_yahoo
    update_TDs_yahoo = SyDB.update_TDs_yahoo
    
    update_TDs = SyDB.update_TDs
    
    #### CORE 

    set_interval =  Syc.set_interval
    
    
    