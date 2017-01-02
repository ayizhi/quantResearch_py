#coding: utf-8

from __future__ import print_function

import datetime
import pprint
try:
	import Queue as queue
except ImportError:
	import queue
import time

class Backtest(object):
	def __init__(self,csv_dir,symbol_list,initial_capital,hearbeat,start_date,data_handler,execution_handler,portfolio,strategy):
		self.csv_dir = csv_dir
		self.symbol_list = symbol_list
		self.initial_capital = initial_capital
		self.hearbeat = hearbeat
		self.start_date = start_date

		self.data_handler_cls = data_handler
		self.execution_handler_cls = execution_handler
		self.portfolio_cls = portfolio
		self.strategy_cls = strategy

		self.events = queue.Queue()

		self.signals = 0
		self.orders = 0
		self.fills = 0
		self.num_strats = 1
		self._generate_trading_instances()

	def _generate_trading_instances(self):
		print("Creating DataHandler, Strategy, Portfolio and ExecutionHandler")

		self.data_handler = self.data_handler_cls(self.events,self.csv_dir,self.symbol_list)
		self.strategy = self.strategy_cls(self.data_handler,self.events)
		self.portfolio = self.portfolio_cls(self.data_handler,self.events,self.start_date,self.initial_capital)
		self.execution_handler = self.execution_handler_cls(self.events)

	def _run_backtest(self):
		i = 0
		while True:
			i += 1
			print (i)
			if self.data_handler.continue_backtest == True:
				self.data_handler.update_bars()
			else:
				break

			while True:
				try:
					event = self.events.get(False)
				except queue.Empty:
					break
				else:
					if event is not None:
						if event.type == 'MARKET':
							self.strategy.calculate_signals(event)
							self.Portfolio.update_timeindex(event)
						elif event.type == 'SIGNAL':
							self.signals += 1
							self.portfolio.update_signal(event)
						elif event.type == 'ORDER':
							self.orders += 1
							self.execution_handler.execute_order(event)
						elif event.type == 'FILL':
							self.fills += 1
							self.portfolio.updatee_fill(event)
			time.sleep(self.hearbeat)

	def _output_performance(self):
		self.portfolio.create_equity_curve_dataframe()
		print ('Creating summary stats...')
		stats = self.Portfolio.output_summary_stats()

		print ('Creating equity curve...')
		print (self.Portfolio.equity_curve.tail(10))
		pprint.pprint(stats)

		print ('Signal: %s' % self.signals)
		print ('Orders: %s' % self.orders)
		print ('Fills: %s' % self.fills)

	def simulate_trading(self):
		self._run_backtest()
		self._output_performance()