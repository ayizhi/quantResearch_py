#coding:utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import datetime
import matplotlib.pyplot as plt

import FeatureUtils


def get_good_feature(ticker_data):
	ticker_data = FeatureUtils.CCI(ticker_data,10)
	ticker_data = FeatureUtils.TL(ticker_data,10)
	ticker_data = FeatureUtils.EVM(ticker_data,10)
	ticker_data = FeatureUtils.SMA(ticker_data,10)
	ticker_data = FeatureUtils.EWMA(ticker_data,10)
	ticker_data = FeatureUtils.ROC(ticker_data,10)
	ticker_data = FeatureUtils.ForceIndex(ticker_data,10)
	ticker_data = FeatureUtils.BBANDS(ticker_data,10)
	ticker_data = ticker_data.dropna()
	#formlization
	ticker_data = (ticker_data - ticker_data.mean())/(ticker_data.max() - ticker_data.min())
	#get today and next day
	X = DataFrame(ticker_data.drop('close',1).fillna(0),dtype='float64')[:-1]
	#y要把后一天的日期跟前一天对其
	y = Series(ticker_data['close'].shift(-1).dropna(),dtype='|S6')

	#forest find the best 5 features
	features = FeatureUtils.forestFindFeature(X,y,100)[:5]
	ticker_data = ticker_data[features]
	return ticker_data









