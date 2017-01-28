#coding:utf-8
import tushare as ts
import MySQLdb as mdb
import datetime


def get_hs300_tickers():
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	with con:
		cur = con.cursor();
		cur.execute('SELECT id,ticker FROM symbol')
		data = cur.fetchall();
		return [(d[0],d[1]) for d in data]

def get_ticker_info_by_id(ticker_id):
	start_date = datetime.datetime(2016,01,01)
	end_date = datetime.today().timetuple()
	tData = ts.get_hist_data(ticker_id,start=start_date,end=end_date,retry_count=5,pause=1)
	return end_date


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
	             close_price, volume, adj_close_price"""
	insert_str = ("%s, " * 11)[:-2]
	final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)
	daily_data = []

	for i in range(len(ticker.index)):
		t_date = ticker.index[i]
		t_data = ticker.ix[t_date]
		daily_data.append(
			(vendor_id, ticker_id, t_date, now, now,t_data['open'], t_data['high']
				, t_data['low'], t_data['close'], t_data['volume'], 0)
		)

	with con:
		cur = con.cursor()
		cur.executemany(final_str, daily_data)
		


print get_ticker_info_by_id(1)