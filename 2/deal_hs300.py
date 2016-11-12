# 股票价格的预测分类/回归模型
# 1. price between 10-50 
# 2. 沪深三百内的 
# 3. average daily volume (ADV) in the middle 33 percentile

import db
from db import get_10_50_by_id,get_tickers_from_db
import datetime 
import time
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt


tickers = get_tickers_from_db()

for i in range(len(tickers)):
	this_ticker = tickers[i]
	ticker_id = this_ticker[0]
	ticker_name = this_ticker[1]
	print ticker_id
	data = get_10_50_by_id(ticker_id);
	g_data = [[data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]] for i in range(len(data))]
	index_list = [data[i][0] for i in range(len(data))]
	one_data = DataFrame(g_data,index=index_list,columns=['open_price','high_price','low_price','close_price','volume'])
	new_data_list = pd.date_range('1/1/2015', '12/31/2015', freq='1D')
	one_data = one_data.reindex(new_data_list,fill_value='0')


	print df





	# pd.join(high_price)
	# pd.join(low_price)
	# pd.join(close_price)
	# pd.join(volume)
	



	break
	


