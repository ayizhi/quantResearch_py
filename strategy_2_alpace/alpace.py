#coding: utf-8
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db

names = [
	'util/NASDAQ.csv',
	'/util/NYSE.csv',
	'/util/AMEX.csv'
]

names = db.get_us_ticker_name_from_csv(names[0])