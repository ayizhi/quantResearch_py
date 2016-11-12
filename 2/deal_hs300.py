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


tickers = get_tickers_from_db()
new_date_list = pd.date_range('1/1/2015', '12/31/2015', freq='1D')
date_list = [str(new_date_list[i])[:10] for i in range(len(new_date_list))]
date_obj = {}
for i in range(len(date_list)):
	day = date_list[i]
	day_volume = sorted(get_day_volumn_33_66(day))
	tlen = len(day_volume)
	if tlen == 0 :
		date_obj[day] = (0,0)
		continue
	t33 = int(tlen * 0.33)
	t66 = int(tlen * 0.66)
	date_obj[day] = (day_volume[t33],day_volume[t66])
print date_obj


# for i in range(len(tickers)):
# 	this_ticker = tickers[i]
# 	ticker_id = this_ticker[0]
# 	ticker_name = this_ticker[1]
# 	print ticker_id
# 	data = get_10_50_by_id(ticker_id);
# 	g_data = [[data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]] for i in range(len(data))]
# 	index_list = [data[i][0] for i in range(len(data))]
# 	one_data = DataFrame(g_data,index=index_list,columns=['open_price','high_price','low_price','close_price','volume'])
# 	one_data = one_data.reindex(new_data_list,fill_value='0')
# 	print df



# 	break
	


