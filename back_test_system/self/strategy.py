from __future__ import print_function
from abc import ABCMeta,abstractmethod
import datetime
try:
	import Queue as queue
except ImportError:
	import queue
import numpy as np
import pandas as pd
from event import SignalEvent

class Strategy(object):
	__metaclass = ABCMeta

	@abstractmethod
	def calculate_signals(self):
		raise NotImplementedError('Should implement calculate_signals()')