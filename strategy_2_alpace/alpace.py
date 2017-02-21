#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db




if __name__ == '__main__':

	day_range = 10 #计算周期
	round_days = 7 #执行周期
	average_days = 7 * 10 #几日均线

	#找到volumn在33％－66%之间的股票池,20日平均交易量,并且
	stockers = db.get_us_middle33_volume(day_range,8,20)
	stocker_ids = stockers['id']
	best_10 = [];
	worst_10 = [];
	

	for i in range(len(stocker_ids)):
		stocker_id = stocker_ids[i]
		end_date = db.get_us_last_date(stocker_id)[0][0]
		start_date = end_date + datetime.timedelta(days = day_range * -1)
		stocker_data = db.get_us_ticker_from_db_by_id(stocker_id,start_date,end_date)
		profit = (stocker_data.loc[0].close - stocker_data.loc[len(stocker_data) - 1].close)/stocker_data.loc[len(stocker_data) - 1].close
		current_price = stocker_data.loc[0].close
		average_price = db.get_average_days_price_by_id(stocker_id,average_days)

		print profit,current_price,average_price,'----------------------'

		#表现最好的,还要高于十周均线
		if len(best_10) > 0 :
			for i in range(len(best_10)):
				if (profit > best_10[i][1]) and profit > 0:
					if len(best_10) >= 10:
						del best_10[i]
					if(current_price > average_price){
						best_10.append((stocker_id,profit))
					}
					continue
		else:
			if profit > 0:
				if(current_price > average_price){
					best_10.append((stocker_id,profit))	
				}

		#表现最差的
		if len(worst_10) > 0:
			for i in range(len(worst_10)):
				if (profit < worst_10[i][1]) and profit < 0:
					if len(worst_10) >= 10:
						del worst_10[i]
					if(current_price < average_price){			
						worst_10.append((stocker_id,profit))
					}
					continue
		else:
			if profit < 0:	
				if(current_price < average_price){	
					worst_10.append((stocker_id,profit))	
				}
		

	print 'best_10: ',best_10
	print '======='
	print 'worst_10: ',worst_10
	
	print '======='

	






