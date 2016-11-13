# 股票价格的预测分类/回归模型
# 1. price between 10-50 
# 2. 沪深三百内的 
# 3. average daily volume (ADV) in the middle 33 percentile

import db
from db import get_10_50_by_id,get_tickers_from_db,get_day_volumn_33_66
import datetime 
import time
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import forecast


def get_33_and_66_volumn(date_list):
	date_list = [str(date_list[i])[:10] for i in range(len(date_list))]
	date_obj = {}
	for i in range(len(date_list)):
		day = date_list[i]
		day_volume = np.mean(np.array(get_day_volumn_33_66(day)))
		if np.isnan(day_volume) :
			continue
		t33 = int(day_volume * 0.33)
		t66 = int(day_volume * 0.66)
		date_obj[day] = (t33,t66)
		print day,day_volume
	return date_obj


tickers = get_tickers_from_db()
new_date_list = pd.date_range('1/1/2015', '12/31/2015', freq='1D')
# daily_volumn = get_33_and_66_volumn(new_date_list)
selected_data = []



for i in range(len(tickers)):
	this_ticker = tickers[i]
	ticker_id = this_ticker[0]
	ticker_name = this_ticker[1]
	data = get_10_50_by_id(ticker_id);
	g_data = []
	index_list = []
	for i in range(len(data)):
		date = data[i][0]
		date = str(date)[0:10]
		volume = data[i][5]
		# volume_range = range(daily_volumn[date][0],daily_volumn[date][1])
		# if volume > daily_volumn[date][0] and volume < daily_volumn[date][1]:
		g_data.append([data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]])
		index_list.append(data[i][0])
	if len(g_data) < 50:
		continue
	t_ticker = DataFrame(g_data,index=index_list,dtype='float64',columns=['open','high','low','close','volume'])
	t_ticker = t_ticker.reindex(new_date_list,method='ffill').fillna(method='bfill')
	selected_data.append(t_ticker)
	#得到表现最好的5个feature下的数据
	t_ticker = forecast.get_good_feature(t_ticker)

	# print t_ticker
	forecast.get_regression_r2(t_ticker)





	break

print len(selected_data)
	


