#coding:utf-8
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts
import FeatureUtils
from FeatureUtils import toDatetime
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier


#获取沪深300股指数据
hs300 = ts.get_hist_data('hs300')
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

print hs300.head(10)



print hs300.index,hs300.columns


