import datetime
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import MySQLdb as mdb
import numpy as np
import statsmodels.tsa.stattools as ts


#get name
def get_tickers_from_db(con):
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall()
		return [(d[0],d[1],d[2]) for d in data]

#get data from 2010 to 2015
def get_2010_2015(ticker_id,ticker_name,con):
		with con:
			cur = con.cursor()
			cur.execute('SELECT price_date,close_price from daily_price where (symbol_id = %s) and (price_date BETWEEN "20100101" AND "20151231")' % ticker_id)
			ticker_data = cur.fetchall()
			dates = np.array([d[0] for d in ticker_data])
			t_data = np.array([d[1] for d in ticker_data])
			ticker_data = np.array(t_data,dtype='float64')
	
		return ticker_data

#hurst
def hurst(ts):
	lags = range(2,100)
	tau = [np.sqrt(np.std(np.subtract(ts[lag:],ts[:-lag]))) for lag in lags]
	poly = np.polyfit(np.log(lags),np.log(tau),1)
	return poly[0] * 2.0



if __name__ == '__main__':
	#connect to db
	db_host = 'localhost'
	db_user = 'root'
	db_pass = ''
	db_name = 'securities_master'
	con = mdb.connect(db_host, db_user, db_pass, db_name)

	#get 300 names and id
	tickers = get_tickers_from_db(con)

	all_hurst_data = []
	all_adf_data = []
	
	#get data of 2010-2015
	for i in range(len(tickers)):
		ticker = tickers[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		ticker_data = get_2010_2015(ticker_id,ticker_name,con)


		#数量太少报maxlag should be < nobs
		if ticker_data.shape[0] < 100:
			continue

		print '========================================'
		print '========================================'
		print '========================================'
		#hust
		t_hurst = hurst(ticker_data)
		if t_hurst < 0.3:
			all_hurst_data.append((ticker_id,ticker_name))
			print 'Hurst %s : %s' % (ticker_name,t_hurst)

		#adf test
		t_adf = ts.adfuller(ticker_data,1)
		if t_adf[0] < t_adf[4]['5%']:
			all_adf_data.append((ticker_id,ticker_name))
			print 'ADF test %s : %s' % (ticker_name,t_adf)
		print '========================================'
		print '========================================'
		print '========================================'



		
	print all_hurst_data
	print all_adf_data



		






