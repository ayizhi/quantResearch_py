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

def get_ticker_info_by_id(id):
	start_date = datetime.datetime(2016,01,01)
	end_date = datetime.today().timetuple()
	return end_date




print get_ticker_info_by_id(1)