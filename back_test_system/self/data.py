from __future__ import print_function
from abc import ABCMeta,abstractmethod

import datetime
import os,os.path

import numpy as np
import pandas as pd

from event import MarketEvent

class DataHandler(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def get_latest_bar(self,symbol):
		raise NotImplementedError("Should implement get_latest_bar()")

	@abstractmethod
	def get_latest_bars(self,symbol,N=1):
		raise NotImplementedError("Should implement get_latest_bars()")

	@abstractmethod
	def get_latest_bar_datetime(self,symbol):
		raise NotImplementedError("Should implement get_latest_bar_datetime()")

	@abstractmethod
	def get_latest_bar_value(self,symbol,val_type):
		raise NotImplementedError("Should implement get_latest_bar_value()")

	@abstractmethod
	def get_latest_bars_value(self,symbol,val_type,N=1):
		raise NotImplementedError("Should implement get_latest_bars_values()")

	def update_bars(self):
		raise NotImplementedError("Should implement update_bars()")


class HistoricCSVDataHandler(DataHandler):

	def __init__(self,events,csv_dir,symbol_list):
		self.events = events
		self.csv_dir = csv_dir
		self.symbol_list = symbol_list

		self.symbol_data = {}
		self.latest_symbol_data = {}
		self.continue_backtest = True
		self.bar_index = 0

		self._open_convert_csv_files()

	def _open_convert_csv_files(self):
		comb_index = None
		for s in self.symbol_list:
			self.symbol_data[s] = pd.io.parsers.read_csv(os.path.join(self.csv_dir,'%s.csv' % s), header=0,index_col=0,parse_dates=True,names=['datetime','open','high','low','close','volume','adj_close']).sort()
			if comb_index is None:
				comb_index = self.symbol_data[s].index
			else:
				comb_index.union(self.symbol_data[s].index)
			self.latest_symbol_data[s] = []

		for s in self.symbol_list:
			self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index,method='pad').iterrows()

	def _get_new_bar(self,symbol):
		for b in self.symbol_data[symbol]:
			yield b

	def get_latest_bar(self,symbol):
		try:
			bars_list = self.latest_symbol_data[symbol]

		except KeyError:
			print ("That symbol is not available in the historical data set.")
			raise

		else:
			return bars_list[-1]

	def get_latest_bars(self,symbol,N=1):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print('That symbol is not available in the historical data set.')
			raise
		else:
			return bars_list[-N:]

	def get_latest_bar_datetime(self,symbol):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return bars_list[-1][0]

	def get_latest_bar_value(self,symbol,val_type):
		try:
			bars_list = self.latest_symbol_data[symbol]
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return getattr(bars_list[-1][1],val_type)

	def get_latest_bars_values(self,symbol,val_type,N=1):
		try:
			bars_list = self.get_latest_bars(symbol,N)
		except KeyError:
			print("That symbol is not available in the historical data set.")
			raise
		else:
			return np.array([getattr(b[1],val_type) for b in bars_list])

	def update_bars(self):
		for s in self.symbol_list:
			try:
				bar = next(self._get_new_bar(s))
			except StopIteration:
				self.continue_backtest = False
			else:
				if bar is not None:
					self.latest_symbol_data[s].append(bar)
		self.events.put(MarketEvent())