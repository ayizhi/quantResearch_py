#coding:utf-8
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts
import FeatureUtils
from FeatureUtils import toDatetime
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC


#获取沪深300股指数据
hs300 = DataFrame(ts.get_hist_data('hs300'))
hs300 = toDatetime(hs300)

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
X = hs300_norm.drop('close',1)
y = np.asarray(hs300_norm['close'], dtype="|S6")

#forest find feature
features = FeatureUtils.forestFindFeature(X,y,10)

X_F = hs300_norm[features[0:10]]

X_train, X_test, y_train, y_test = train_test_split(X_F, y, test_size=0.5, random_state=42)

print X_train.head(10)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}]

# Perform the grid search on the tuned parameters
model = GridSearchCV(SVC(C=1), tuned_parameters, cv=10)
print X_train.shape,y_train.shape

# for i in range(X_train.shape[0]):
# 	print X_train.ix[i].shape
model.fit(X_train, y_train)

# print("Optimised parameters found on training set:")
# print(model.best_estimator_, "\n")

# print("Grid scores calculated on training set:")
# for params, mean_score, scores in model.grid_scores_:
# 	print("%0.3f for %r" % (mean_score, params))


