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

###########################################
########### Moving Averages ###############
###########################################


def get_BollingerBand (self, L = 20):
    ## Get the Bollinger Bands !!

    price = self.get_timeSeries(["Close"])
    
    MA = self.get_SMA(L = L)
    diff = np.power(price - MA, 2);# Get the difference to the square

#    print MA.shape
#    print price.shape
#    print diff.shape

    diff_SMA = indl.get_SMA(diff, L)  # Get the avera STD over L periods
    diff_SMA = 2 * np.sqrt(diff_SMA)
    
    # Now we apply a MA over this shit
    
    return diff_SMA
    
def get_RSI(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1] # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

