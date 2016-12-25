#coding:utf-8
#对沪深三百股票进行聚类，并画出关系图
import tushare as ts
import sqlalchemy as create_engine
import MySQLdb as mdb
import datetime



def get_tickers_from_db(con):
	#get name form symbol;
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker FROM symbol')
		data = cur.fetchall()
		return [(d[0],d[1]) for d in data]

def get_hist_data_from_tushare(ticker):
	start_date = '2000-1-1'
	end_date = str(datetime.date.today().timetuple())
	
	#get every detail data
	tData = ts.get_hist_data(ticker,start=start_date,end=end_date,retry_count=5,pause=1)
	return tData

def into_db(tTicker,data,data_vendor_id,con):
	# Create the time now
	now = datetime.datetime.utcnow()
	 # Create the insert strings
	column_str = """data_vendor_id, symbol_id, price_date, created_date, 
	             last_updated_date, open_price, high_price, low_price, 
	             close_price, volume, adj_close_price"""
	insert_str = ("%s, " * 11)[:-2]
	final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)
	daily_data = []

	for i in range(len(data.index)):
		t_date = data.index[i]
		t_data = data.ix[t_date]
		daily_data.append(
			(data_vendor_id, tTicker, t_date, now, now,t_data['open'], t_data['high']
				, t_data['low'], t_data['close'], t_data['volume'], 0)
		)

	with con:
		cur = con.cursor()
		cur.executemany(final_str, daily_data)



if __name__ == '__main__':
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)

	#get history data and put them into database
	tickers = get_tickers_from_db(con);

	#iterating every ticker and put theirs data into datbase
	for i in range(len(tickers)):
		t = tickers[i]
		tTicker = tickers[i][1]
		data = get_hist_data_from_tushare(tTicker)
		data_vendor_id = i
		print 'data_vendor_id : %s' % data_vendor_id
		print 'tTicker : %s' % tTicker
		print '%s of %s' % (i,len(tickers))
		into_db(tTicker,data,data_vendor_id,con)






