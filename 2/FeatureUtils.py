import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import tushare as ts



def CCI(data,ndays):
	TP = (data['high'] + data['low'] + data['close'])/3 
	CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015 * pd.rolling_std(TP, ndays)),name='CCI')
	return CCI

#timeLag
def TL(data,ndays):
	pH = pd.Series([data['high'][i:i+ndays].max() for i in range(len(data.index))],index=data.index,dtype='float64')
	pL = pd.Series([data['low'][i:i+ndays].max() for i in range(len(data.index))],index=data.index,dtype='float64')
	pO = pd.Series([data['open'][i] - data['open'][i-1] for i in range(len(data.index))],index=data.index,dtype='float64')
	timeLag = pd.Series(pO/(pH - pL),name='TimeLag')
	return timeLag

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




hs300 = pd.DataFrame(ts.get_hist_data('hs300'))
hs300.index = pd.to_datetime(hs300.index)

timeLag = TL(hs300,20)
CCI = CCI(hs300,20)


print hs300['close']



