import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt


def 

def CCI(data,ndays):
	TP = (data['high'] + data['low'] + data['close'])/3