import pandas as pd

import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier


#CCI
def CCI(data,ndays):
	TP = (data['high'] + data['low'] + data['close'])/3 
	CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015 * pd.rolling_std(TP, ndays)),name='CCI')
	data = data.join(CCI)
	return data

#timeLag
def TL(data,ndays):
	index = data.index
	pH = data['high'].resample(str(ndays) + 'D').max().reindex(index).fillna(method='bfill')
	pL = data['low'].resample(str(ndays) + 'D').max().reindex(index).fillna(method='bfill')
	pO = data['open'] - data['open'].shift(1)
	timeLag = pO/(pH - pL)
	timeLag.name = 'TL'
	data = data.join(timeLag)
	return data


#Ease of Movement
def EVM(data,ndays):
	dm = ((data['high'] + data['low'])/2) - ((data['high'].shift(1) + data['low'].shift(1))/2)
	br = (data['volume']/100000000)/((data['high'] - data['low']))
	EVM = dm/br
	EVM_MA = pd.Series(pd.rolling_mean(EVM,ndays),name='EVM')
	data = data.join(EVM_MA)
	return data

# Simple Moving Average 
def SMA(data, ndays): 
	SMA = pd.Series(pd.rolling_mean(data['close'], ndays), name = 'SMA') 
	data = data.join(SMA)
	return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
	EMA = pd.Series(pd.ewma(data['close'], span = ndays, min_periods = ndays - 1), 
	name = 'EWMA_' + str(ndays))  
	data = data.join(EMA)
	return data


# Rate of Change (ROC)
def ROC(data,n):
	N = data['close'].diff(n)
	D = data['close'].shift(n)
	ROC = pd.Series(N/D,name='Rate of Change')
	data = data.join(ROC)
	return data 

# Force Index 
def ForceIndex(data, ndays): 
	FI = pd.Series(data['close'].diff(ndays) * data['volume'], name = 'ForceIndex') 
	data = data.join(FI)
	return data

# Compute the Bollinger Bands 
def BBANDS(data, ndays):
	MA = pd.Series(pd.rolling_mean(data['close'], ndays)) 
	SD = pd.Series(pd.rolling_std(data['close'], ndays))
	b1 = MA + (2 * SD)
	B1 = pd.Series(b1, name = 'Upper BollingerBand') 
	b2 = MA - (2 * SD)
	B2 = pd.Series(b2, name = 'Lower BollingerBand') 
 	data = data.join([B1,B2])
 	return data



def plotTwoData(data1,data2):
	fig = plt.figure(figsize=(7,5))
	ax = fig.add_subplot(2, 1, 1)
	ax.set_xticklabels([])
	plt.plot(data1,lw=1)
	plt.title(str(data1.name) + 'Price Chart')
	plt.ylabel('Close Price')
	plt.grid(True)
	bx = fig.add_subplot(2, 1, 2)
	plt.plot(data2,'k',lw=0.75,linestyle='-',label='CCI')
	plt.legend(loc=2,prop={'size':9.5})
	plt.ylabel(str(data2.name) + 'values')
	plt.grid(True)
	plt.setp(plt.gca().get_xticklabels(), rotation=30)
	plt.show()



def toDatetime(data):
	data.index = pd.to_datetime(data.index)
	return data



def forestFindFeature(X,y,n):

	# Build a forest and compute the feature importances
	forest = ExtraTreesClassifier(n_estimators=n,random_state=0)
	forest.fit(X, y)
	importances = forest.feature_importances_
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
	indices = np.argsort(importances)[::-1]

	#Print the feature ranking
	print("Feature ranking:")

	x_columns = X.columns
	features = []
	for f in range(X.shape[1]):
		features.append(x_columns[int(indices[f])])
		print f,indices[f],x_columns[int(indices[f])],'===========', importances[indices[f]]
		# print("%d. feature %d (%f)" % (f + 1,indices[f], importances[indices[f]]))



	## Plot the feature importances of the forest
	# plt.figure()
	# plt.title("Feature importances")
	# plt.bar(range(X.shape[1]), importances[indices],
	#        color="r", yerr=std[indices], align="center")
	# plt.xticks(range(X.shape[1]), indices)
	# plt.xlim([-1, X.shape[1]])
	# plt.show()
	return features




