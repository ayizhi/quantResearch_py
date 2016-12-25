import MySQLdb as mdb
import csv


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
	csvFile = file('./data/%s.csv' % ticker_id,'wb')
	writer = csv.writer(csvFile)
	writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume', 'adj_close'])
	writer.writerows(data)
	csvFile.close()	




