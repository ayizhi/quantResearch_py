import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint

import os
path = os.getcwd()
print path

data = pd.read_csv(path + '/hs.csv',parse_dates=True,iterator=True)
data = pd.DataFrame(data.get_chunk(1000))
print data
