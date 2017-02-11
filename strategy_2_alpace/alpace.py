#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db


if __name__ == '__main__':
	symbols = db.get_us_tickers();
	start_date = '1/1/2015'
	for i in range(len(symbols)):
		symbol = symbols[i][1];
		print '========= loading %s , %s ==========' % (i,symbol)
		ticker = db.get_us_ticker_by_id(symbol,start_date)
		print '========= loading success'
		db.save_us_ticker_into_db(symbol,ticker,i)
		break