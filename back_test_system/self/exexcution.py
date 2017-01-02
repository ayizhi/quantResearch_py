from __future__ import print_function

from abc import ABCMeta,abstractmethod
import datetime
try:
	import Queue as queue
except ImportError:
	import queue

from event import FillEvent,OrderEvent

class ExecutionHandler(object):
	__metaclass = ABCMeta

	@abstractmethod
	def execute_order(self,event):
		raise NotImplementedError('Should implement execute_order()')

class SimulateExecutionHandler(ExecutionHandler):
	def  __init__(self,events):
		self.evnets = events

	def execute_order(self,event):
		if event.type == 'ORDER':
			fill_event = FillEvent(
				datetime.datetime.utcnow(),event.symbol,'ARCA',event.quantity,event.direction,None)
			self.events.put(fill_event)