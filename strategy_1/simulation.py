#coding: utf-8
import numpy as np
import pandas as pd

import sys
sys.path.append('..')
import util.db as db


if __name__ == '__main__':
	ticker_df = db.get_ticker_from_db_by_id('300133')
	ticker_index = ticker_df['index']
	ticker_np = np.array(ticker_df[['open','high','low','close','volume']])
	ticker_df = pd.DataFrame(ticker_np,index=ticker_index,columns=['open','high','low','close','volume'])