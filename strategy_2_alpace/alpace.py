#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db




if __name__ == '__main__':

	#找到volumn在33％－66%之间的股票池,20日平均交易量
	stockers = db.get_us_middle33_volume(20)
	stocker_ids = stockers['id']
	print stocker_ids


