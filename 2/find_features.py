#coding:utf-8
import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts
import FeatureUtils
from FeatureUtils import toDatetime
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier


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
x_columns = X.columns


# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=10000,
                              random_state=0)
forest.fit(X, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]


# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
	print f,indices[f],x_columns[int(indices[f])],'===========', importances[indices[f]]
	# print("%d. feature %d (%f)" % (f + 1,indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()







