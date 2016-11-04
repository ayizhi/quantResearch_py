#coding:utf-8
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts
import FeatureUtils
from FeatureUtils import toDatetime
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.metrics import r2_score
from sklearn import linear_model
import datetime



#获取沪深300股指数据
hs300 = DataFrame(ts.get_hist_data('hs300'))
hs300 = toDatetime(hs300).dropna()

#加入feature
hs300 = FeatureUtils.CCI(hs300,10)
hs300 = FeatureUtils.TL(hs300,10)
hs300 = FeatureUtils.EVM(hs300,10)
hs300 = FeatureUtils.SMA(hs300,10)
hs300 = FeatureUtils.EWMA(hs300,10)
hs300 = FeatureUtils.ROC(hs300,10)
hs300 = FeatureUtils.ForceIndex(hs300,10)
hs300 = FeatureUtils.BBANDS(hs300,10)
hs300 = hs300.dropna()

#归一化
hs300_norm = (hs300 - hs300.mean())/(hs300.max() - hs300.min())

# # Build a classification task using 3 informative features
X_real = DataFrame(hs300_norm.drop('close',1),dtype='|S6')
X = X_real.shift(periods = -1).dropna()
y_real = Series(hs300_norm['close'],dtype='|S6')
y = y_real[:-1]

print X.shape,y.shape,'=========='


#forest find feature
features = FeatureUtils.forestFindFeature(X,y,1000)

X_real_F = DataFrame(hs300_norm[features[0:10]],dtype='|S6')
X_F = X_real_F.shift(periods = -1).dropna()
y_F = Series(y,dtype='|S6')
X_F = FeatureUtils.toDatetime(X_F)
y_F = FeatureUtils.toDatetime(y_F)

d = datetime.datetime(2015,12,31)

print X_F.shape,y_F.shape

X_train = X_F[X.index < d]
X_test = X_F[X.index >= d]
y_train = y_F[y.index < d]
y_test = y_F[y.index >= d]

print X_train.shape,X_test.shape,y_train.shape,y_test.shape

# Create the (parametrised) models
print("Hit Rates/Confusion Matrices:\n")
models = [
	('LR',LinearRegression()),
	('RidgeR',Ridge (alpha = 0.005)),
	('lasso',Lasso(alpha=0.0001)),
	('LassoLars',LassoLars(alpha=0.0001))
]

for m in models:
	m[1].fit(X_train,y_train)
	pred = m[1].predict(X_test)
	print "%s:\n%0.3f" % (m[0], r2_score(y_test,pred))


model = Lasso(alpha=0.001)
model.fit(X_train, y_train)
pred = model.predict(X_test)
pred_test = pd.Series(pred, index=y_test.index)
print(r2_score(y_test,pred_test))
fig  = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(y_test,'r',lw=0.75,linestyle='-',label='realY')
ax.plot(pred_test,'b',lw=0.75,linestyle='-',label='predY')
plt.legend(loc=2,prop={'size':9})
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.grid(True)
plt.show()