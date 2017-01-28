#coding: utf-8

from db import get_hs300_tickers,get_ticker_info_by_id,save_ticker_into_db
import datetime


if __name__ == '__main__':
	ticker_info = get_hs300_tickers()
	for i in range(len(ticker_info)):
		ticker = ticker_info[i]
		ticker_id = ticker[1]
		vendor_id = i;
		ticker_data = get_ticker_info_by_id(ticker_id)
		print ticker_data
		break
