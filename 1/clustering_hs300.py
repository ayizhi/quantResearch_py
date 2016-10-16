#coding:utf-8
#对沪深三百股票进行聚类，并画出关系图
import tushare as ts
import sqlalchemy as create_engine

import MySQLdb as mdb




#get hs300's names
hs300 = ts.get_hs300s()
for i in range(len(hs300)):
	tHs = {};
	tHs = hs300.ix[i,['name','code']];
	print tHs['name'],tHs['code'];

	#get every detail data
	tData = ts.get_hist_data(tHs['code'],start='2016-01-01',end='2016-10-15')
	print tData


