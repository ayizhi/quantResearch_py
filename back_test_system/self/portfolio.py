from __future__ import print_function

import datetime
from math import floor
try:
	import Queue as queue
except ImportError:
	import queue
import numpy as np
import pandas as pd

from event import FillEvent,OrderEvent
from performance import create_sharpe_ratio,create_drawdowns


class Portfolio(object):
	def __init__(self,bars,event,start_date,intial_capital=100000.0):
		self.bars = bars
		self.events = events
		self.symbol_list = self.bars.symbol_list
		self.start_date = start_date
		self.intial_capital = intial_capital
		self.all_positions = self.construct_all_positions()
		self.current_positions = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
		self.all_holdings = self.construct_all_holdings()
		self.current_holdings = self.construct_current_holdings()

	def construct_all_positions(self):
		d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
		d['datetime'] = self.start_date
		return [d]

	def construct_all_holdings(self):
		d = dict((k,v) for k,v in [(s,0.0) for s in self.symbol_list])
		d['datetime'] = self.start_date
		d['cash'] = self.intial_capital
		d['commission'] = 0.0
		d['total'] = self.intial_capital
		return [d]

	def construct_current_holdings(self):
		d = dict((k,v) for k,v in [(s,0.0) for s in self.symbol_list])
		d['cash'] = self.intial_capital
		d['commission'] = 0.0
		d['total'] = self.intial_capital
		return d

	def update_timeindex(self,event):
		latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])

		# Update positions
        # ================
		dp = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
		dp['datetime'] = latest_datetime

		for s in self.symbol_list:
			dp[s] = self.current_positions[s]

		self.all_positions.append(dp)

		# Update holdings
        # ===============
		dh = divt((k,v) for k,v in [(s,0) for s in self.symbol_list])

		dh['datetime'] = latest_datetime
		dh['cash'] = self.current_holdings['cash']
		dh['commission'] = self.current_holdings['commission']
		dh['total'] = self.current_holdings['cash']

		for s in self.symbol_list:
			market_value = self.current_positions[s] * self.bars.get_latest_bar_value(s,'close')
			dh[s] = market_value
			dh['total'] += market_value

		self.all_holdings.append(dh)

	# =======================
	# FILL/POSITION HANDLING
	# =======================

	def update_positions_from_fill(self,fill):
		fill_dir = 0
		if fill.direction == 'BUY':
			fill_dir = 1
		if fill.direction == 'SELL':
			fill_dir = -1
		self.current_positions[fill.symbol] += fill_dir * fill.quantity

	def update_holdings_from_fill(self,fill):
		fill_dir = 0
		if fill_direction == 'BUY':
			fill_dir = 1
		if fill.direction == 'SELL':
			fill_dir = -1
		fill_cost = self.bars.get_latest_bar_value(fill.symbol,'adj_close')
		cost = fill_dir * fill_cost * fill.quantity
		self.current_holdings[fill.symbol] += cost
		self.current_holdings['commission'] += fill.commission
		self.current_holdings['cash'] -= (cost + fill.commission)
		self.current_holdings['total'] -= (cost + fill.commission)

	def update_fill(self,event):
		if event.type == 'FILL':
			self.update_positions_from_fill(event)
			self.update_holdings_from_fill(event)

	def generate_naive_order(self,signal):
		order = None

		symbol = signal.symbol
		direction = signal.signal_type
		strength = signal.strength

		mkt_quantity = 100
		cur_quantity = self.current_positions[symbol]
		order_type = 'MKT'

		if direction == 'LONG' and cur_quantity == 0:
			order = OrderEvent(symbol,order_type,mkt_quantity,'BUY')
		if direction == 'SHORT' and cur_quantity == 0:
			order = OrderEvent(symbol,order_type,mkt_quantity,'SELL')
		if direction == 'EXIT' and cur_quantity > 0:
			order = OrderEvent(symbol,order_type,abs(cur_quantity),'SELL')
		if direction == 'EXIT' and cur_quantity < 0:
			order = OrderEvent(symbol,order_type,abs(cur_quantity),'BUY')

		return order

	def update_signal(self,event):
		if event.type == 'SIGNAL':
			order_event = self.generate_naive_order(event)
			self.events.put(order_event)


    # ========================
    # POST-BACKTEST STATISTICS
    # ========================

	def create_equity_curve_dataframe(self):
		curve = pd.DataFrame(self.all_holdings)
		curve.set_index('datetime',inplace=True)
		curve['returns'] = curve['total'].pct_change()
		curve['equity_curve'] = (1.0 * curve['returns']).cumprod()
		self.equity_curve = curve

	def output_summary_stats(self):
		total_return = self.equity_curve['equity_curve'][-1]
		returns = self.equity_curve['returns']
		pnl = self.equity_curve['equity_curve']

		print (total_return,returns,pnl)

		sharpe_ratio = create_sharpe_ratio(returns,periods=252 * 60 * 6.5)
		drawdown,max_dd,dd_duration = create_drawdowns(pnl)
		self.equity_curve['drawdown'] = drawdown

		stats = [('Total Return','%0.2f%%' % ((total_return - 1.0) * 100.0)),('Sharpe Ratio','%0.2f' % sharpe_ratio),('Max Drawdown','%0.2f%%' % (max_dd * 100.0)),('Drawdown Duration','%d' % dd_duration)]

		self.equity_curve.to_csv('equity.csv')

		return stats

