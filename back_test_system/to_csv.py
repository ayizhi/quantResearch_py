import MySQLdb as mdb
import csv
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import sys

def get_tickers_from_db():
	db_host = 'localhost'
	db_user = 'root'
	db_pd = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_pd, db=db_name)
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker FROM symbol');
		return cur.fetchall()


def get_one_ticker_by_id(ticker_id):
	db_host = 'localhost'
	db_user = 'root'
	db_pd = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_pd, db=db_name)
	with con:
		cur = con.cursor()
		cur.execute('SELECT price_date,open_price,high_price,low_price,close_price,volume FROM daily_price WHERE symbol_id = %s' % ticker_id)
		return cur.fetchall()


def render_csv(ticker_id):
	data = get_one_ticker_by_id(ticker_id)

	np_data = np.array(data)
	pd_data = DataFrame(np_data,columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
	adj_close = Series([d[4] for d in data])
	pd_data['adj_close'] = adj_close
	pd_data.to_csv('./data/%s.csv' % ticker_id)	


render_csv('600050')






