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
		self.events = events
		self.short_window = short_window
		self.long_window = long_window

		self.bought = self._calculate_initial_bought()

	def _calculate_initial_bought(self):
		bought = {}
		for s in self.symbol_list:
			bought[s] = 'OUT'
		return bought

	def calculate_signals(self,event):
		if event.type == 'MARKET':
			for symbol in self.symbol_list:
				bars = self.bars.get_latest_bars_values(symbol,'close',N=self.long_window)
				if bars is not None and bars != []:
					short_sma = np.mean(bars[-self.short_window:])
					long_sma = np.mean(bars[-self.long_window:])

					dt = self.bars.get_latest_bar_datetime(symbol)
					sig_dir = ''
					strength = 1.0
					strategy_id = 1

					if short_sma > long_sma and self.bought[symbol] == 'OUT':
						sig_dir = 'LONG'
						signal = SignalEvent(strategy_id,symbol,dt,sig_dir,strength)
						self.events.put(signal)
						self.bought[symbol] = 'LONG'
					elif short_sma < long_sma and self.bought[symbol] == 'LONG':
						sig_dir = 'EXIT'
						signal = SignalEvent(
							strategy_id,symbol,dt,sig_dir,strength)
						self.events.put(signal)
						self.bought[symbol] = 'OUT'

if __name == '__main__':
	csv_dir = 'data'
	symbol_list = ['600050']
	initial_capital = 100000.0
	start_date = datetime.datetime(1990,1,1,0,0,0)
	hearbeat = 0.0

	backtest = Backtest(
		csv_dir,symbol_list,
		initial_capital,
		hearbeat,
		start_date,
		HistoricCSVDataHandler,
		SimulateExecutionHandler,
		Portfolio,
		MovingAverageCrossStrategy
		)
	 backtest.simulate_trading()

