#coding:utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import datetime
import matplotlib.pyplot as plt
import Feature_utils
#回归
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.metrics import r2_score
from sklearn import linear_model
#分类
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.qda import QDA
from sklearn.svm import LinearSVC, SVC


def get_regression_r2(ticker_data):
	data_len = len(ticker_data)
	split_line = int(data_len * 0.2)
	X = ticker_data.drop('close',1).shift(-10).dropna()
	y = ticker_data['close'][:-10].dropna()

	X_test = X.ix[:split_line]
	X_train = X.ix[split_line:]
	y_test = y.ix[:split_line]
	y_train = y.ix[split_line:]

	models = [
	('LR',LinearRegression()),
	('RidgeR',Ridge (alpha = 0.005)),
	('lasso',Lasso(alpha=0.00001)),
	('LassoLars',LassoLars(alpha=0.00001))]

	best_r2 = (models[0][1],0)
	for m in models:
		m[1].fit(np.array(X_train),np.array(y_train))
		pred = m[1].predict(X_test.fillna(0))
		r2 = r2_score(y_test,pred)
		if r2 > best_r2[1]:
			best_r2 = (m[1],r2)
		# print "%s:\n%0.3f" % (m[0], r2_score(np.array(y_test),np.array(pred)))

	print 'the best regression is:',best_r2

	model = best_r2[0]
	model.fit(X_train, y_train)
	pred = model.predict(X_test.fillna(0))
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


def get_classification_r2(ticker_data):


	data_len = len(ticker_data)
	split_line = int(data_len * 0.8)
	X = ticker_data.drop('close',1)[:-1]
	y = Series(ticker_data['close'].shift(-1).dropna(),dtype='|S6')

	X_train = X.ix[:split_line]
	X_test = X.ix[split_line:]
	y_train = y.ix[:split_line]
	y_test = y.ix[split_line:]


 	models = [("LR", LogisticRegression()),
		("LDA", LDA()),
		("LSVC", LinearSVC()),
		("RSVM", SVC(
			C=1000000.0, cache_size=200, class_weight=None,
		coef0=0.0, degree=3, gamma=0.0001, kernel='rbf',
		max_iter=-1, probability=False, random_state=None,
		shrinking=True, tol=0.001, verbose=False)
		),
		("RF", RandomForestClassifier(
			n_estimators=1000, criterion='gini',
		max_depth=None, min_samples_split=2,
		min_samples_leaf=1, max_features='auto',
		bootstrap=True, oob_score=False, n_jobs=1,
		random_state=None, verbose=0)
	)]

	best = (0,0)
	for m in models:
		m[1].fit(X_train, y_train)
		pred = m[1].predict(X_test)
		name = m[0]
		score = m[1].score(X_test, y_test)
		if score > best[1]:
			best = (name,score)
	print 'the best cluster is:' , best
	return best


