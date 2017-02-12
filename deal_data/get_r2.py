import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
import os
path = os.getcwd()
print path
import FeatureUtils
import forecast
from pandas import Series,DataFrame

#回归
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn import linear_model


data = pd.read_csv(path + '/2/hs.csv',parse_dates=True,iterator=True)
# data = pd.read_csv(path + '/2/hs.csv',parse_dates=True)
data = pd.DataFrame(data.get_chunk(5000),dtype='|S6')
# data = pd.DataFrame(data,dtype='|S6')



def get_regression_r2(ticker_data):
	data_len = len(ticker_data)
	split_line = int(data_len * 0.8)
	X = ticker_data.drop('realY',1)
	y = ticker_data['realY'].dropna()

	X_train = X.ix[:split_line]
	X_test = X.ix[split_line:]
	y_train = y.ix[:split_line]
	y_test = y.ix[split_line:]

	models = [
	# ('LR',LinearRegression()),
	# ('RidgeR',Ridge (alpha = 0.005)),
	# ('lasso',Lasso(alpha=0.00001)),
	# ('LassoLars',LassoLars(alpha=0.00001)),
	('RandomForestRegression',RandomForestRegressor(1000))]

	best_r2 = ('',-10000000)

	for m in models:
		m[1].fit(np.array(X_train),np.array(y_train))
		#因为index方面，pred出的其实是相当于往后挪了一位，跟原来的y_test是对不上的，所以x需要往前进一位
		#比较绕，所以从日期对应的方面去考虑
		pred = m[1].predict(X_test.shift(-1).fillna(0))
		r2 = r2_score(y_test,pred)
		if r2 > best_r2[1]:
			best_r2 = (m[1],r2)
		# print "%s:\n%0.3f" % (m[0], r2_score(np.array(y_test),np.array(pred)))

	print 'the best regression is:',best_r2

	model = best_r2[0]
	model.fit(X_train, y_train)
	pred = model.predict(X_test.shift(-1).fillna(0))
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


X = data.drop(['realY','predictY'],1)
y = data['realY']

#get importances of features
# features = FeatureUtils.forestFindFeature(X,y,100)[:300]

data = X.join(y)

get_regression_r2(data)


# print data