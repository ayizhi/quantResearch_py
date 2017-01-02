import datetime
import numpy as np

from backtest import Backtest
from data import HistoricCSVDataHandler
from event import SignalEvent
from execution import SimulateExecutionHandler
from portfolio import Portfolio
from strategy import Strategy

class MovingAverageCrossStrategy(Strategy):
	def __init__(self,bars,events,short_window=100,long_window=400):
		self.bars = bars
		self.symbol_list = self.bars.symbol_list
		self.evnets = events
		self.short_window = short_window
		self.long_window = long_window

		self.bought = self._calculate_initial_bought()