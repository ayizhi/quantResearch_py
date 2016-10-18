import datetime
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import MySQLdb as mdb

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
			ticker_data = DataFrame(t_data,index=dates,columns=[ticker_name],dtype='float64')

	

		return ticker_data

#deal data
def deal_with_data(all_data):
	all_data = np.array(all_data)
	print all_data.shape


if __name__ == '__main__':
	#connect to db
	db_host = 'localhost'
	db_user = 'root'
	db_pass = ''
	db_name = 'securities_master'
	con = mdb.connect(db_host, db_user, db_pass, db_name)

	#get 300 names and id
	tickers = get_tickers_from_db(con)

	all_data = []

	#get data of 2010-2015
	for i in range(len(tickers)):
		ticker = tickers[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		ticker_data = get_2010_2015(ticker_id,ticker_name,con)
		all_data.append(ticker_data)

	deal_with_data(all_data)



