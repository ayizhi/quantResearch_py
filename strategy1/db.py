#coding:utf-8
import tushare as ts
import MySQLdb as mdb
import datetime
import time

#获取事先储存过的300支股票
def get_hs300_tickers():
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	with con:
		cur = con.cursor();
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall();
		return [(d[0],d[1],d[2]) for d in data]

#根据id获取ticker
def get_ticker_info_by_id(ticker_id):
	df = ts.get_stock_basics()
	start_date = df.ix[ticker_id]['timeToMarket'] #上市日期YYYYMMDD
	start_date = str(start_date)
	start_date_year = start_date[0:4]
	start_date_month = start_date[4:6]
	start_date_day = start_date[6:8]
	start_date = start_date_year + '-' + start_date_month + '-' + start_date_day
	end_date = str(datetime.date.today())
	ticker_data = ts.get_h_data(ticker_id,start=start_date,end=end_date,retry_count=10,pause=1)
	return ticker_data

#读取symbol表里的last_update_date
def get_last_updated_date(ticker_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	with con:
		cur = con.cursor();
		cur.execute("SELECT last_updated_date from symbol where ticker=%s" % ticker_id )
		date = cur.fetchall()
		return date

#更新symbol表里的last_update_date
def fresh_last_updated_date(ticker_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	now = datetime.datetime.utcnow()
	with con:
		cur = con.cursor();
		cur.execute("""UPDATE symbol SET last_updated_date='%s' where ticker=%s"""%(now,ticker_id))


#储存到数据库
def save_ticker_into_db(ticker_id,ticker,vendor_id):
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	# Create the time now
	now = datetime.datetime.utcnow()
	 # Create the insert strings
	column_str = """data_vendor_id, symbol_id, price_date, created_date,
	              last_updated_date, open_price, high_price, low_price,
	              close_price, volume, amount, adj_close_price"""
	insert_str = ("%s, " * 12)[:-2]
	final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)
	daily_data = []

	print ticker.index


	for i in range(len(ticker.index)):
		print i,'====='
		t_date = ticker.index[i]
		t_data = ticker.ix[t_date]
		daily_data.append(
			(vendor_id, ticker_id, t_date, now, now,t_data['open'], t_data['high']
				, t_data['low'], t_data['close'], t_data['volume'], t_data['amount'],0)
		)

		break;

	with con:
		cur = con.cursor()
		cur.executemany(final_str, daily_data)


