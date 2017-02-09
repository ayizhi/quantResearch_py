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
	start_date = datetime.datetime(2016,1,1)
	end_date = datetime.datetime.today()
	ticker_df = ticker_df[ticker_df.index >= start_date]
	ticker_df = ticker_df[ticker_df.index <= end_date]
	ticker_data = get_good_feature(ticker_df,10)
	ticker_data.dtype = '|S6'



	#get best ml
	get_regression_r2(ticker_data)

