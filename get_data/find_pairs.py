# coding:utf-8
import matplotlib.pyplot as plt
import MySQLdb as mdb
import datetime
import numpy as np
from pandas import Series,DataFrame
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold
from pandas.stats.api import ols
import statsmodels.tsa.stattools as ts
import sys   
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')   
  
#找到有协整关系的pairs

def plot_price_series(df, ts1, ts2):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2016, 5, 1), datetime.datetime(2016, 10, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()

def plot_scatter_series(df, ts1, ts2):
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.show()


#get name
def get_tickers_from_db(con):
	#get name form symbol;
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall()
		return [(d[0],d[1],d[2]) for d in data]

#get daily data of 300
def get_daily_data_from_db(ticker,ticker_name,ticker_id,date_list,con):
	with con:
		cur = con.cursor()
		cur.execute('SELECT price_date,open_price,high_price,low_price,close_price,volume from daily_price where symbol_id = %s' % ticker_id)
		daily_data = cur.fetchall()
		dates = np.array([d[0] for d in daily_data])
		#此处以受益为基准
		# open_price = np.array([d[2] for d in daily_data],dtype='float64')
		close_price = np.array([d[4] for d in daily_data],dtype='float64')
		# var_price = close_price - open_price
		# daily_data = DataFrame(var_price,index=dates,columns=[ticker_id])

		daily_data = DataFrame(close_price,index=dates,columns=[ticker_name])
		daily_data = daily_data.reindex(date_list,method='ffill')
		return daily_data


#dealing data with two-pair way to calculating
def deal_data(whole_data):
	finall_pair = []
	print '正在计算... '

	for i in range(len(whole_data)):
		for r in range(i,len(whole_data)):

			if i == r:
				continue


			d1 = whole_data[i].fillna(method='pad').fillna(0)
			d1_name = d1.columns[0]
			d2 = whole_data[r].fillna(method='pad').fillna(0)
			d2_name = d2.columns[0]
			df = pd.concat([d1,d2],axis=1)

			res = ols(y=d1[d1_name], x=d2[d2_name])
			beta_hr = res.beta.x
			df["res"] = df[d1_name] - beta_hr*df[d2_name]
			cadf = ts.adfuller(df["res"])

			#judge比较cadf那俩值的大小
			cadf1 = cadf[0]
			cadf2 = cadf[4]['5%']
			#这样更明显
			if cadf1 - cadf2 < -4 :
				print '得到结果=======>>>>>>',i,r,cadf1,cadf2,d1_name,d2_name
				finall_pair.append((i,r))
				test(i,r)

	return finall_pair

#处理最终pair数据
def deal_with_fianl_data(whole,pairs):
	names = [];
	final = [];
	for i in range(len(whole)):
		name = whole[i].columns[0]
		names.append(name)
	for r in range(len(pairs)):
		t = pairs[r]
		name1 = names[t[0]]
		name2 = names[t[1]]
		final.append((name1,name2))
	return final

def test(d1,d2):
	d1 = whole_data[d1].fillna(method='pad').fillna(0)
	d1_name = d1.columns[0]
	d2 = whole_data[d2].fillna(method='pad').fillna(0)
	d2_name = d2.columns[0]
	df = pd.concat([d1,d2],axis=1)
	plot_price_series(df, d1.columns[0], d2.columns[0])
	plot_scatter_series(df,d1.columns[0], d2.columns[0])



if __name__ == '__main__':
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	date_list = pd.date_range('5/1/2016', '10/1/2016', freq='1D')
	tickers = get_tickers_from_db(con)
	whole_data = []

	for i in range(len(tickers)):
		ticker = tickers[i]
		ticker_name = ticker[2]
		ticker_id = ticker[1]
		daily_data = get_daily_data_from_db(ticker,ticker_name,ticker_id,date_list,con)
		whole_data.append(daily_data)

	#dealing data with two-pair way to calculating
	final_pair = deal_data(whole_data)

	#整理最终结果，因为finall－pair返回的是序号
	pairs = deal_with_fianl_data(whole_data,final_pair)

	
	print pairs



