# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 23:55:37 2016

@author: montoya
"""
#
import import_folders
import pandas as pd
import numpy as np
import DDBB_lib as DBl
import CCAPM as CCAPM
import CBond as CBond

import datetime as dt
import numpy as np
import CTimeData as CTD
import copy as copy
import utilities_lib as ul
from yahoo_finance import Share
import CPortfolio as CPfl
import utilities_lib as ul
import matplotlib.pyplot as plt

from graph_lib import gl
plt.close("all")
##########################################################
############### DOWNLOADING ALL THE DDBB ###############
##########################################################

### All the info of the symbols
#symbols = ['AMD', 'BAC', 'MSFT', 'TXN']


symbols = [
            'SCHW',  # The Charles Schwab Corporation. Finance
           'AAPL',  # Apple
#           'MSFT',  # Microsoft
           'TAP',   # Molson Coors Brewing Company 

           'LUV',   # Southwest Airlines
           'CAT',   # Caterpillar Inc. (CAT) Construction
           'SPY',    #SPDR S&P 500 ETF ()
           'TXN',  # Texas Instruments Incorporated 
#           'AMD',
#           'BAC',     
           
#           'MON',   # Monsanto Company. Quemicals
#           'RAI',   # Reynolds American Inc. Tobacco
]

mktcap = dict()
mktcap['SCHW'] = 51.38
mktcap['AAPL'] = 585.81
mktcap['MSFT'] = 460.69
mktcap['TAP'] = 19.08
mktcap['LUV'] = 29.49
mktcap['CAT'] = 55.66
mktcap['SPY'] = 194.65
mktcap['TXN'] = 70.68

#symbols = ['AMD', 'TXN','TAP', 'SPY']
#symbols = ['AMD', 'BAC', 'MSFT', 'TXN']

sdate = "01-01-1997"
edate = "01-11-2016"
period = 43200          # Monthly period
periods = [period]

timeData = CTD.CTimeData('MSFT',period)  # Init a timeSeries

# Play a little with yahoo finance
#yahoo = Share(symbols[0])
#print yahoo.get_info()

storage_folder = "./storage/Yahoo/"
## Check if we download it or use the one we have
download = 0
if (download == 1):
    # This code is only for one symbol, for the portfolio,
    # go down bitch.
    timeData.download_from_yahoo(sdate,edate)
    timeData.add_csv(storage_folder)  ## Add it to the one we already have
    timeData.save_to_csv(storage_folder)
    
else: 
    timeData.set_csv(storage_folder)

basic_TD_op = 0
if (basic_TD_op == 1):
    ## BASIC TD operatons
    timeData = CTD.CTimeData(symbols[3],period)
    timeData.update_csv_yahoo(sdate,edate)
    timeData.set_interval(dt.datetime(2010,1,5),dt.datetime(2016,1,1))
    
    price = timeData.get_timeSeries(["RangeHL","RangeCO"]);
    dates = timeData.get_dates()
    
    timeData.plot_timeSeries(nf = 1)
    price2 = timeData.get_timeSeries(["magicDelta"]);
    timeData.plot_timeSeries()
    
#    timeData.plot_dailyHA()

##########################################################
############### PORTFOLIO THINGS !!! ######################
##########################################################

Cartera = CPfl.Portfolio(symbols, periods)   # Set the symbols and periods to load
#Cartera.update_symbols_csv_yahoo(sdate,edate,storage_folder)    # Load the symbols and periods
Cartera.load_symbols_csv(storage_folder)
#Cartera.set_interval(dt.datetime(1996,12,5),dt.datetime(2016,2,21))

##########################################################
############### CAPM model !!! ######################
##########################################################
## Load the porfolio in the CAPM model
CAPMillo = CCAPM.CAPM(Cartera, period)
CAPMillo.set_allocation([])
CAPMillo.set_Rf(0.0)
CAPMillo.set_seriesNames(["Adj Close"])  # Adj Close 
CAPMillo.set_index('SPY')
CAPMillo.set_interval(sdate,edate)

#CAPMillo.set_seriesNames(["Close"])
basic_func = 0
if (basic_func == 1):
    ## Plot an examples return correlation
    CAPMillo.plot_retCorr(symbols[0], symbols[1])
    
    ## Set an initial allocation
    ## Simulate and simulate the Portfolio
    CAPMillo.simulate_Portfolio()
    CAPMillo.simulate_Portfolio(mode = "normal")
    

## Get some efficient frontier and simulate the portfolio
rand_alloc = 0
if (rand_alloc == 1):
    
    gl.set_subplots(2,2)
    Nalloc = 100
    
    #1
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "yes", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8, legend = ["Normal alloc"])
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Tangent", max_exp = 100.0)
    CAPMillo.plot_allocations(portfolios, legend = ["Normal Eff"], nf = 0)
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)

    #2
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "Lintner", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8,nf = 1, legend = ["Lintner alloc"])
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Lintner")
    CAPMillo.plot_allocations(portfolios, legend = ["Lintner Eff"], nf = 0)
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)

    #3
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "no", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8,nf = 1, legend = ["Markovitz alloc"])
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Markowitz")
    CAPMillo.plot_allocations(portfolios, legend = ["Markowitz Eff"], nf = 0)
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)

    #4
    # WARNING !! The calculation of the efficient frontier this way could be
    # wrong if the covariance matrix is not good enough.
#    ## Frontier and portfolios when we allow short sales.
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "yes", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8, legend = ["Normal alloc"])
    
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Tangent", max_exp = 10.0)
    CAPMillo.plot_allocations(portfolios, legend = ["Normal Eff"], nf = 0)

    ## Frontier and portfolios when we allow short sales but constained in 
    ## in the sum of the absolute values.
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "Lintner", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8,nf = 0, legend = ["Lintner alloc"])
    
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Lintner")
    CAPMillo.plot_allocations(portfolios, legend = ["Lintner Eff"], nf = 0)
#    
    # Get the efficient frontier where we cannot borrow or lend money
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "no", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8,nf = 0, legend = ["Markovitz alloc"])
    
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Markowitz")
    CAPMillo.plot_allocations(portfolios, legend = ["Markowitz Eff"], nf = 0)

    # Scatter Assets
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)


rand_alloc_2 = 0

if (rand_alloc_2 == 1):
    # Other way for finding efficient frontier
    # Scatter random porfolio so that the sum of all the allocation is 1

#    portfolios = CAPMillo.TangenPortfolioFrontier(norm = "none", maxRf = 0.0032)
#    CAPMillo.scatter_allocations(portfolios, nf = 1)

#    portfolios = CAPMillo.TangenPortfolioFrontier2(norm = "none", maxRf = 0.01)
#    CAPMillo.scatter_allocations(portfolios, nf = 1)

    Nalloc = 100000
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "yes", mode = "gaussian")
    
    CAPMillo.scatter_allocations(alloc, alpha = 0.8, legend = ["Normal alloc"])
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Tangent")
    CAPMillo.plot_allocations(portfolios, legend = ["Normal Efficient Eff"], nf = 0)

    # Scatter Assets
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)

CAPM_model = 0
if (CAPM_model == 1):
    CAPMillo.set_allocation([])
    CAPMillo.set_Rf(0.0)
    
    CAPMillo.set_index(symbols[0])
    param = CAPMillo.get_symbol_ab(symbols[1])
    print param
    
    params = CAPMillo.get_all_symbols_ab()
    print params
    
    param = CAPMillo.get_portfolio_ab(mode = "normal")    
    print param
    
    param = CAPMillo.get_portfolio_ab(mode = "gaussian")    
    print param
    
    JensenAlpha = CAPMillo.get_portfolio_JensenAlpha()
    
    ## IDEA !! Maybe use the portfolio in the frontier that maximizes
    ## the alpha and minimizes the beta !!! Maybe minimizing beta is not as important
    ## In the CAMP we already have the total Exp and risk.
    ## Alpha and beta say: Does out portolio perform better than the market ?
    ## If we just follow the market, investing everything on the index,
    ## Thus investing in everything proportionally to their capital.
    ## Then we have alpha = 0 and beta = 1 
#    CAPMillo.test_symbol_ab(symbols[2])
    CAPMillo.test_Jensens_Alpha()
    
    # Do it again with an optimal portolio
    w = CAPMillo.TangentPortfolio(Rf = 0.0)
    CAPMillo.set_allocation(w)
    CAPMillo.test_Jensens_Alpha()
    
    print "Market Timing "
    print CAPMillo.get_portfolio_ab()

####################################################
#### Examples model !!!
####################################################

examples_F = 0
if (examples_F == 1):
    
    # Do some examples with portfolio
    Rf = 0.001
    ## INIT Portfolio
    CAPMillo = CCAPM.CAPM(Cartera, period)
    CAPMillo.set_allocation([])
    CAPMillo.set_Rf(Rf)
    
    ## Simulate stupid portolio
    CAPMillo.simulate_Portfolio()

    ## Now lets do a proper portfolio
    # Get the optimal porfolio (short allowed)
    w = CAPMillo.TangentPortfolio(Rf = Rf)
    CAPMillo.set_allocation(w)
    CAPMillo.simulate_Portfolio()

    ## Now change the Rf
    Rf = 0.00
    CAPMillo.set_Rf(Rf)
    w = CAPMillo.TangentPortfolio(Rf = Rf)
    CAPMillo.set_allocation(w)
    CAPMillo.simulate_Portfolio()
    

BL_f = 0
if (BL_f == 1):
    # Take the values from He & Litterman, 1999.
    
    # Calculate initial portfolio from the market capitalization
    mc = [317957301, 556812224, 532667693, 1703857627, 989410674]
    weq = [0.15,0.25,0.1,0.28,0.22]

    Sigma = [[0.04881,	0.03311,	0.03080,	0.04534,	0.03998],
            [0.03311,	0.04129,	0.02939,	0.03777,	0.03321],
            [0.03080,	0.02939,	0.03406,	0.03804,	0.03348],
            [0.04534,	0.03777,	0.03804,	0.06446,	0.04618],
            [0.03998,	0.03321,	0.03348,	0.04618,	0.04839]]
    
    # Study !!!
    # We are assuming efficiency. The amount of money in a place
    # accounts for its risk. So the weights have the return..

    # Risk aversion of the market 
    delta = 2  # Names gamma of A by the professor.
    # Almost increases linearly the Posterior return.
    # It also depends in the prior Q and Omega
    # It is close to the fucking sharpe ratio.
    # delta = (Rp - Rf)/Sigma_p^2.
    # If we multipy w by a constant (we like more risk).
    # And the delta increases.
    
    Sigma_shit  = np.sqrt(np.dot(np.dot(weq,Sigma),weq))
    
    # Coefficient of uncertainty in the prior estimate of the mean
    tau = 0.3
    ### Prior of out Views !!!
    P1 = [[ -1,	1,	0,	0,	0],
          [ 0, -1	,1,	0,	0]]
    P1 = ul.fnp(P1)
    
    # If we invert P1 and Q1 at the same time we get the same
    Q1 = [-0.02, -0.01]
    Q1 = ul.fnp(Q1)
    
    Omega1 = np.dot(np.dot(P1,Sigma),P1.T) * np.eye(Q1.shape[0])
    
    res = CAPMillo.BlackLitterman(weq, Sigma, delta, # Prior portfolio variables
                   tau,              # Uncertainty coefficient of the porfolio priors
                   P1, Q1, Omega1)   # Prior views variables
    
    # Reference returns of the portfolio of the market
    # They can just be calculated using the portfolio
    refPi = delta * np.dot(Sigma, weq)              
    
    print refPi  # Expected returns wihout priors
    print res[0] # Expected returns after priors
    
    # A priory the expected return Posteriori does not have to be bigger
    # Just more accuarate to reality if our views are right :)
    Ereturn = np.dot(refPi,weq)
    EreturnPost = np.dot(res[0],res[1])
    
    print Ereturn
    print EreturnPost
#    display('View 1',assets,res)
    

IFE = 1
if (IFE == 1):
    param = CAPMillo.IFE_a()
#    param = CAPMillo.IFE_b()
#    param = CAPMillo.IFE_c()
#    param = CAPMillo.IFE_d(Rf = 0.01, 
#                           Rfs_list = [-0.007,-0.003,-0.0015,0,0.0015,0.003,0.007,])
#    param = CAPMillo.IFE_e(ObjectiveR = 0.003, Rf = 0.0)
#    param = CAPMillo.IFE_f(ObjectiveR = 0.01, Rf = 0.0)
#    param = CAPMillo.IFE_f2(ObjectiveRlist = np.linspace(0.0001,0.01, 15), Rf = 0.0)
#    param = CAPMillo.IFE_g(Rf = 0.0)
#    param = CAPMillo.IFE_h(Rf = 0.0, mktcap = mktcap)
#    param = CAPMillo.IFE_i(Rf = 0.0)

#    CAPMillo.IFE_2a()
#    CAPMillo.IFE_2b()
#    CAPMillo.IFE_2c()
    pass
