from db import get_us_tickers,get_us_ticker_from_db_by_id,save_us_ticker_into_db,get_us_last_date
import datetime
import db
import tushare as ts
import pandas as pd
import time



if __name__ == '__main__':
	#hs300的id
	ticker_info = get_us_tickers()
	for i in range(len(ticker_info)):
		ticker = ticker_info[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		vendor_id = i;

		# if i < :
		# 	continue

		print '--------------------- %s ---------------------' % vendor_id

		try:
			print '========= loading %s , %s ==========' % (i,ticker_id)
			start_date = get_us_last_date(ticker_id)[0][0]
			print '========= loading success =========='
			start_date = start_date + datetime.timedelta(days = 1)
			
		except:
			start_date = ''

		print start_date , '============================================'
		
		try:
			ticker_data = db.get_us_ticker_by_id(ticker_id,start_date)
		except:
			print 'get data fail...'
			ticker_data = pd.DataFrame([])

		print ('data :' , ticker_data)

		if ticker_data.shape[0] != 0:
			#存储
			
			try:
				print '+++++++++++++ save %s , %s success +++++++++++++++' % (i,ticker_id)				
				save_us_ticker_into_db(ticker_id,ticker_data,vendor_id)
			except:
				print(ticker_id, 'is error')
		
		print ticker_id,'==== finished ====='
		



