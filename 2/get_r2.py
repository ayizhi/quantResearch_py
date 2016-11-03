import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
path = os.getcwd()
print path

data = pd.read_csv(path + '/2/HFT_XY_unselected.csv',encoding='gbk')
print data