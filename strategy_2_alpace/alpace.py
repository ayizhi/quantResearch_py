#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db
import pprint.pprint as pprint




if __name__ == '__main__':

	day_range = 20 #计算周期
	round_days = 7 #执行周期
	average_days = 7 * 10 #几日均线

	#找到volumn在33％－66%之间的股票池,20日平均交易量,并且
	stockers = db.get_us_middle33_volume(day_range,8,20)
	stocker_ids = stockers['id']
	np_best_50 = np.array([])
	np_worst_10 = np.array([])
	np_all = np.array([])
	#需要计算的，方差，30周均线，计算周期趋势
	

	for i in range(len(stocker_ids)):
		stocker_id = stocker_ids[i]
		end_date = db.get_us_last_date(stocker_id)[0][0]
		start_date = end_date + datetime.timedelta(days = day_range * -1)
		stocker_data = db.get_us_ticker_from_db_by_id(stocker_id,start_date,end_date)
		profit = (stocker_data.loc[0].close - stocker_data.loc[len(stocker_data) - 1].close)/stocker_data.loc[len(stocker_data) - 1].close
		current_price = stocker_data.loc[0].close
		mean_price, std_price = db.get_average_days_price_by_id(stocker_id,average_days)

		if current_price > mean_price :
			np.all.append((stocker_id,current_price,profit,mean_price,std_price))
		

		print profit,current_price,mean_price,std_price,'----------------------'

	pprint(np_all)




	






