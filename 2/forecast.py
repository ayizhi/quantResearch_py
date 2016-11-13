#coding:utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import datetime
import matplotlib.pyplot as plt
import FeatureUtils
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.metrics import r2_score
from sklearn import linear_model


def get_good_feature(ticker_data):
	ticker_data = FeatureUtils.CCI(ticker_data,10)
	ticker_data = FeatureUtils.TL(ticker_data,10)
	ticker_data = FeatureUtils.EVM(ticker_data,10)
	ticker_data = FeatureUtils.SMA(ticker_data,10)
	ticker_data = FeatureUtils.EWMA(ticker_data,10)
	ticker_data = FeatureUtils.ROC(ticker_data,10)
	ticker_data = FeatureUtils.ForceIndex(ticker_data,10)
	ticker_data = FeatureUtils.BBANDS(ticker_data,10)
	ticker_data = ticker_data.dropna()
	#formlization
	ticker_data = (ticker_data - ticker_data.mean())/(ticker_data.max() - ticker_data.min())
	#get today and next day
	X = DataFrame(ticker_data.drop('close',1).fillna(0),dtype='float64')[:-1]
	#y要把后一天的日期跟前一天对其
	y = Series(ticker_data['close'].shift(-1).dropna(),dtype='|S6')
	#forest find the best 11 features
	features = FeatureUtils.forestFindFeature(X,y,100)[:11]

	ticker_data = ticker_data[features].join(ticker_data['close'])
	return ticker_data

def get_regression_r2(ticker_data):
	data_len = len(ticker_data)
	split_line = int(data_len * 0.8)
	X = ticker_data.drop('close',1)[:-1]
	y = ticker_data['close'].shift(-1).dropna()

	X_train = X.ix[:split_line]
	X_test = X.ix[split_line:]
	y_train = y.ix[:split_line]
	y_test = y.ix[split_line:]

	models = [
	('LR',LinearRegression()),
	('RidgeR',Ridge (alpha = 0.005)),
	('lasso',Lasso(alpha=0.00001)),
	('LassoLars',LassoLars(alpha=0.00001))]

	best_r2 = (0,0)
	for m in models:
		m[1].fit(np.array(X_train),np.array(y_train))
		#因为index方面，pred出的其实是相当于往后挪了一位，跟原来的y_test是对不上的，所以需要往前进一位
		pred = m[1].predict(X_test).shift(-1).fillna(0)
		r2 = r2_score(y_test)
		if r2 > best_r2[1]:
			best_r2 = (m[0],r2)
		print "%s:\n%0.3f" % (m[0], r2_score(y_test,pred))
	print 'the best is:',best_r2

	model = Lasso(alpha=0.0001)
	model.fit(X_train, y_train)
	pred = model.predict(X_test).shift(-1).fillna(0)
	pred_test = pd.Series(pred, index=y_test.index)
	fig  = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.plot(y_test,'r',lw=0.75,linestyle='-',label='realY')
	ax.plot(pred_test,'b',lw=0.75,linestyle='-',label='predY')
	plt.legend(loc=2,prop={'size':9})
	plt.setp(plt.gca().get_xticklabels(), rotation=30)
	plt.grid(True)
	plt.show()

	return best_r2









