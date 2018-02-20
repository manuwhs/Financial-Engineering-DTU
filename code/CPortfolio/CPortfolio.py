import Portfolio_DDBB as Pdb
import Portfolio_core as CPc
import CSymbol as CSy
import Portfolio_operations as CPop
import Portfolio_interface as CPin

class Portfolio:
    def __init__(self, symbol_names = [], periods = [], symbols_list = []):
        self.set_symbols_names(symbol_names);
        self.set_periods(periods);   # Quite useless I would say. Maybe used to specify data to load in a future
        self.symbols = dict()
        # Loop over the symbol_names so loop over all the symbols in the Portfolio

        if (symbols_list != []):  # If we are given both the names and the list
            self.set_symbols(symbols_list)
        else:
            self.init_symbols()  # Create the symbol objects from the periods and names
            
    # secutities will be a dictionary of [symbol]
    set_symbols = CPc.set_symbols
    set_symbols_names = CPc.set_symbols_names
    
    set_periods = CPc.set_periods
    init_symbols = CPc.init_symbols
    
    set_intraRange = CPc.set_intraRange
    set_dailyRange  = CPc.set_dailyRange
    
    set_interval = CPc.set_interval
    get_dates = CPc.get_dates
    get_timeSeries = CPc.get_timeSeries
    get_Returns = CPc.get_Returns
    get_CumReturns = CPc.get_CumReturns
    
    get_dailyReturns = CPc.get_dailyReturns
    get_dailyCumReturns = CPc.get_dailyCumReturns
    #######################################################################
    #### DDBB Operations ##################################################
    #######################################################################
           
    update_symbols_csv = Pdb.update_symbols_csv
    load_symbols_csv = Pdb.load_symbols_csv
    save_to_csv = Pdb.save_to_csv
    update_symbols_csv_yahoo = Pdb.update_symbols_csv_yahoo
    download_symbols_csv_yahoo = Pdb.download_symbols_csv_yahoo
    
    #######################################################################
    #### Operations over all the prices of the portfolio ##################
    #######################################################################

    get_daily_symbolsPrice = CPop.get_daily_symbolsPrice
    plot_daily_symbolsPrice = CPop.plot_daily_symbolsPrice
    get_daily_symbolsCumReturn = CPop.get_daily_symbolsCumReturn
    
    get_intra_by_days = CPin.get_intra_by_days
    