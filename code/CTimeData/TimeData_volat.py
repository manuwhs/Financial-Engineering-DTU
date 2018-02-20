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

""" OTHER INDICATORS """

def get_drawdown(self):  # TODO
    """
    calculate max drawdown and duration
 
    Returns:
        drawdown : vector of drawdwon values
        duration : vector of drawdown duration
    """
    cumret = pnl
 
    highwatermark = [0]
 
    idx = pnl.index
    drawdown = pd.Series(index = idx)
    drawdowndur = pd.Series(index = idx)
 
    for t in range(1, len(idx)) :
        highwatermark.append(max(highwatermark[t-1], cumret[t]))
        drawdown[t]= (highwatermark[t]-cumret[t])
        drawdowndur[t]= (0 if drawdown[t] == 0 else drawdowndur[t-1]+1)
 
    return drawdown, drawdowndur


    
    