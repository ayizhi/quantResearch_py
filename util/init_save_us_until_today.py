#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
import util.db as db


if __name__ == '__main__':
	symbols = db.get_us_tickers();
	start_date = datetime.datetime(2015,1,1)
	error_arr = [];
	for i in range(len(symbols)):
		symbol = symbols[i][1];
		try:
			print '========= loading %s , %s ==========' % (i,symbol)
			ticker = db.get_us_ticker_by_id(symbol,start_date)
			print '========= loading success'

			db.save_us_ticker_into_db(symbol,ticker,i)
			print '+++++++++++++ save %s , %s success +++++++++++++++' % (i,symbol)
		except:
			error_arr.append(symbol)
			db.delete_symbol_from_db_by_id(symbol)
			print '------------- delete %s , %s success -------------' % (i,symbol)

