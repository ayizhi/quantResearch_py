import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint

import os
path = os.getcwd()
print path

data = pd.read_csv(path + '/2/hs.csv',parse_dates=True)
data = pd.DataFrame(data)
print data.shape
