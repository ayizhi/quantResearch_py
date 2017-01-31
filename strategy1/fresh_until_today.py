from db import get_hs300_tickers,get_ticker_info_by_id,save_ticker_into_db,get_last_date
import datetime


if __name__ == '__main__':
	#hs300的id
	ticker_info = get_hs300_tickers()
	for i in range(len(ticker_info)):
		ticker = ticker_info[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		vendor_id = i;
		start_date = str(get_last_date(ticker_id)[0][0] + datetime.timedelta(days = 1))[0:10]

		#获取
		ticker_data = get_ticker_info_by_id(ticker_id,start_date)

		#存储
		if ticker_data != None:
			save_ticker_into_db(ticker_id,ticker_data,vendor_id)

