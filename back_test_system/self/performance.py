from __future__ import print_function
import numpy as np
import pandas as pd

def create_sharpe_ratio(returns,period=252):
	return np.sqrt(period) * (np.mean(returns)) / np.std(returns)

def create_drawdowns(pnl):
	hwm = [0]
	idx = pnl.index
	drawdown = pd.Series(index = idx)
	duration = pd.Series(index = idx)

	for t in range(1,len(idx)):
		hwm.append(max(hwm[t - 1],pnl[t]))
		drawdown[t] = (hwm[t] - pnl[t])
		duration[t] = (0 if drawdown[t] == 0 else duration[t - 1] + 1)

	return drawdown,drawdown.max(),duration.max()
