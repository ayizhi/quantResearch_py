#coding:utf-8
import tushare as ts
import MySQLdb as mdb
import datetime
import time
import numpy as np
import pandas as pd

def save_hs300_into_db():
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'ticker_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	now = datetime.datetime.utcnow()
	hs300 = ts.get_hs300s()
	column_str = """ticker, instrument, name, sector, currency, created_date, last_updated_date"""
	insert_str = ("%s, " * 7)[:-2]
	final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
	symbols = []

	for i in range(len(hs300)):
		t = hs300.ix[i]
		symbols.append(
			(
				t['code'],
				'stock',
				t['name'],
				'',
				'RMB',
				now,
				now,
				)
			)
	cur = con.cursor()
	with con:
		cur = con.cursor()
		cur.executemany(final_str, symbols)
	print 'success insert hs300 into symbol!'

#获取事先储存过的300支股票
def get_hs300_tickers():
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'ticker_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	with con:
		cur = con.cursor();
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall();
		return [(d[0],d[1],d[2]) for d in data]

#根据id获取ticker
def get_ticker_info_by_id(ticker_id,start_date,end_date=str(datetime.date.today())):
	#如果没传，则默认为该支股票开始的位置
	if start_date == '':
		df = ts.get_stock_basics()
		start_date = df.ix[ticker_id]['timeToMarket'] #上市日期YYYYMMDD
		start_date = str(start_date)
		start_date_year = start_date[0:4]
		start_date_month = start_date[4:6]
		start_date_day = start_date[6:8]
		start_date = start_date_year + '-' + start_date_month + '-' + start_date_day

	print ('======= loading：%s to %s , %s ========' % (start_date,end_date,ticker_id))
	ticker_data = ts.get_h_data(ticker_id,start=start_date,end=end_date,retry_count=50,pause=1)
	print ('======= loading success =======')
	return ticker_data

#读取symbol表里的最新的日期
def get_last_date(ticker_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'ticker_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	with con:
		cur = con.cursor()
		cur.execute("SELECT price_date FROM daily_price WHERE symbol_id=%s ORDER BY price_date DESC" % ticker_id)
		date = cur.fetchall()
		return date


#储存到数据库
def save_ticker_into_db(ticker_id,ticker,vendor_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'ticker_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	# Create the time now
	now = datetime.datetime.utcnow()
	 # Create the insert strings
	column_str = """data_vendor_id, symbol_id, price_date, created_date,
	              last_updated_date, open_price, high_price, low_price,
	              close_price, volume, amount"""
	insert_str = ("%s, " * 11)[:-2]
	final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)
	daily_data = []


	for i in range(len(ticker.index)):
		t_date = ticker.index[i]
		t_data = ticker.ix[t_date]
		daily_data.append(
			(vendor_id, ticker_id, t_date, now, now,t_data['open'], t_data['high']
				, t_data['low'], t_data['close'], t_data['volume'], t_data['amount'])
		)


	with con:
		cur = con.cursor()
		cur.executemany(final_str, daily_data)


#从数据中获取数据
def get_ticker_from_db_by_id(ticker_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'ticker_master'
	con = mdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_name)
	with con:
		cur = con.cursor()
		cur.execute('SELECT price_date,open_price,high_price,low_price,close_price,volume from daily_price where symbol_id = %s' % ticker_id)
		daily_data = cur.fetchall()
		daily_data_np = np.array(daily_data)
		daily_data_df = pd.DataFrame(daily_data_np,columns=['index','open','high','low','close','volume'])

		return daily_data_df

