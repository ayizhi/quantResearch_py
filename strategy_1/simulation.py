#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db
from util.Feature_utils import get_good_feature
from util.ml_util import get_classification_r2,get_regression_r2


if __name__ == '__main__':
	ticker_df = db.get_ticker_from_db_by_id('300133')
	ticker_index = ticker_df['index']
	ticker_np = np.array(ticker_df[['open','high','low','close','volume']])
	ticker_df = pd.DataFrame(ticker_np,index=ticker_index,columns=['open','high','low','close','volume'],dtype="float")
	start_date = str(datetime.datetime(2016,1,1))[0:10]
	end_date = str(datetime.datetime(2017,1,1))[0:10]
	ticker_df = ticker_df[start_date : end_date]
	ticker_data = get_good_feature(ticker_df,10)
	ticker_data.dtype = '|S6'

	#get best ml
	get_regression_r2(ticker_data)


	# Build a classification task using 3 informative features
	X = ticker_data.drop('close',1)
	# X = X_real.shift(1).dropna()
	y = ticker_data['close']
	# y = y_real[:-1]

	d = datetime.datetime(2016,7,10)


	X_train = X[X.index < d]
	X_test = X[X.index >= d]
	y_train = y[y.index <= d]
	y_test = y[y.index > d]


