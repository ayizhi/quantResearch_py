#coding:utf-8
#对沪深三百股票进行聚类，并画出关系图
import tushare as ts
import sqlalchemy as create_engine
import MySQLdb as mdb
import datetime



#get hs300's names and insert them into database
def get_hs300(con):
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
		


if __name__ == '__main__':
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)

	#get all 300 names and put them into database
	get_hs300(con);



