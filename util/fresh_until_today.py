from db import get_hs300_tickers,get_ticker_info_by_id,save_ticker_into_db,get_last_date
import datetime
import tushare as ts
import time


if __name__ == '__main__':
	#hs300的id
	ticker_info = get_hs300_tickers()
	for i in range(len(ticker_info)):
		ticker = ticker_info[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		vendor_id = i;

		print '--------------------- %s ---------------------' % vendor_id

		try:
			start_date = get_last_date(ticker_id)[0]
			start_date = str(start_date[0] + datetime.timedelta(days = 1))[0:10]
		except:
			start_date = ''


		ticker_data = get_ticker_info_by_id(ticker_id,start_date)

		print ('data_shape:' , ticker_data.shape)

		if ticker_data.shape[0] != 0:
			#存储
			try:
				save_ticker_into_db(ticker_id,ticker_data,vendor_id)
			except:
				print '数据有问题！'



