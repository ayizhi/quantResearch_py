# coding:utf-8
import matplotlib.pyplot as plt
import MySQLdb as mdb
import datetime
import numpy as np
from pandas import Series,DataFrame
import pandas as pd
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold
import sys   
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')   
  



#get name
def get_tickers_from_db(con):
	#get name form symbol;
	with con:
		cur = con.cursor()
		cur.execute('SELECT id,ticker,name FROM symbol')
		data = cur.fetchall()
		return [(d[0],d[1],d[2]) for d in data]


#read dataset from db
def get_timeline_from_db(ticker,ticker_name,ticker_id,date_list,con):
	with con:
		cur = con.cursor()
		cur.execute('SELECT price_date,open_price,high_price,low_price,close_price,volume from daily_price where symbol_id = %s' % ticker_id)
		daily_data = cur.fetchall()
		dates = np.array([d[0] for d in daily_data])
		open_price = np.array([d[2] for d in daily_data],dtype='float64')
		close_price = np.array([d[4] for d in daily_data],dtype='float64')
		var_price = close_price - open_price
		daily_data = DataFrame(var_price,index=dates,columns=[ticker_name])
		daily_data = daily_data.reindex(date_list,method='ffill')

		return daily_data

#deal data
def deal_with_data(whole_data):

	#concat
	final = pd.concat(whole_data,axis=1)
	#fix data
	final = final.fillna(method='ffill')

	#由于太慢算得慢，所以改
	final = final.ix[-150:]
	print final

	return final

#clustering
def cluster_data(data):
	names = data.columns
	edge_model = covariance.GraphLassoCV()
	data = np.array(data)

	X = data.copy().T
	X /= X.std(axis=0)


	edge_model.fit(X)
	_, labels = cluster.affinity_propagation(edge_model.covariance_)
	n_labels = labels.max()
	

	for i in range(n_labels + 1):
		print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))
	

	#Visualization
	node_position_model = manifold.LocallyLinearEmbedding(n_components=2, eigen_solver='dense', n_neighbors=6)
	embedding = node_position_model.fit_transform(X.T).T
	plt.figure(1, facecolor='w', figsize=(10, 8))
	plt.clf()
	ax = plt.axes([0., 0., 1., 1.])
	plt.axis('off')

	# Display a graph of the partial correlations
	partial_correlations = edge_model.precision_.copy()
	d = 1 / np.sqrt(np.diag(partial_correlations))
	partial_correlations *= d
	partial_correlations *= d[:, np.newaxis]
	non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)

	# Plot the nodes using the coordinates of our embedding
	plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels,cmap=plt.cm.spectral)

	# Plot the edges
	start_idx, end_idx = np.where(non_zero)
	#a sequence of (*line0*, *line1*, *line2*), where::
	#            linen = (x0, y0), (x1, y1), ... (xm, ym)
	segments = [[embedding[:, start], embedding[:, stop]] for start, stop in zip(start_idx, end_idx)]
	values = np.abs(partial_correlations[non_zero])
	lc = LineCollection(segments,zorder=0, cmap=plt.cm.hot_r,norm=plt.Normalize(0, .7 * values.max()))
	lc.set_array(values)
	lc.set_linewidths(15 * values)
	ax.add_collection(lc)

	# Add a label to each node. The challenge here is that we want to
	# position the labels to avoid overlap with other labels
	for index, (name, label, (x, y)) in enumerate(zip(names, labels, embedding.T)):
		name = str(name).decode('utf-8').encode('utf-8')  
		print name
		dx = x - embedding[0]
		dx[index] = 1
		dy = y - embedding[1]
		dy[index] = 1
		this_dx = dx[np.argmin(np.abs(dy))]
		this_dy = dy[np.argmin(np.abs(dx))]
		if this_dx > 0:
			horizontalalignment = 'left'
			x = x + .002
		else:
			horizontalalignment = 'right'
			x = x - .002
		if this_dy > 0:
			verticalalignment = 'bottom'
			y = y + .002
		else:
		    verticalalignment = 'top'
		    y = y - .002
		plt.text(x, y, name , size=10,horizontalalignment=horizontalalignment,verticalalignment=verticalalignment,bbox=dict(facecolor='w',edgecolor=plt.cm.spectral(label / float(n_labels)),alpha=.6))

	plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
	         embedding[0].max() + .10 * embedding[0].ptp(),)
	plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
	         embedding[1].max() + .03 * embedding[1].ptp())

	plt.show()




if __name__ == '__main__':
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'securities_master'
	con = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
	whole_data = []
	#all tickers
	tickers = get_tickers_from_db(con)
	#由于太慢算得慢，所以改
	date_list = pd.date_range('1/1/2014', '12/31/2016', freq='1D')

	for i in range(len(tickers)):
		ticker = tickers[i]
		ticker_name = ticker[2]
		ticker_id = ticker[1]
		daily_data = get_timeline_from_db(ticker,ticker_name,ticker_id,date_list,con)
		whole_data.append(daily_data)

	final_data = deal_with_data(whole_data)
	# cluster data
	cluster_data(final_data)






