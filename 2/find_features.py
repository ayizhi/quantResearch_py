#coding:utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import MySQLdb as mdb
import tushare as ts

#获取沪深300股指数据
hs300 = ts.get_hist_data('hs300')


print hs300.index,hs300.columns


