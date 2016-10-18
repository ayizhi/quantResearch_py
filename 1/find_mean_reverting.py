import datetime
import pandas as pd
import MySQLdb as mdb

#get name
def get_tickers_from_db(con):
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall()
		return [(d[0],d[1],d[2]) for d in data]

#get data from 2010 to 2015
def get_2010_2015(tickers,con):

	for i in range(len(tickers)):
		ticker = tickers[i]
		ticker_id = ticker[1]
		ticker_name = ticker[2]
		print ticker_id,ticker_name

		with con:
			cur = con.cursor()
			cur.execute('SELECT price_date,close_price from daily_price where (symbol_id = %s) and (price_date BETWEEN "20100101" AND "20151231")' % ticker_id)
			daily_data = cur.fetchall()
			daily_data = [[d[0],ticker_id,ticker_name,d[1]] for d in daily_data]

			print len(daily_data)
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
		print '=========================='
			




if __name__ == '__main__':
	#connect to db
	db_host = 'localhost'
	db_user = 'root'
	db_pass = ''
	db_name = 'securities_master'
	con = mdb.connect(db_host, db_user, db_pass, db_name)

	#get 300 names and id
	tickers = get_tickers_from_db(con)
	#get data of 2010-2015
	get_2010_2015(tickers,con)


