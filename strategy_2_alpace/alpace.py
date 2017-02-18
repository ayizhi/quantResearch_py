#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db




if __name__ == '__main__':

	stockers = db.get_us_tickers()
	for i in range(len(stockers)):
		stocker_id = stockers[i][1]
		print '=========== %s ==== %s ==========' % (stocker_id,i)
		
		stocker = db.get_us_ticker_from_db_by_id(stocker_id)
		print stocker
		break

