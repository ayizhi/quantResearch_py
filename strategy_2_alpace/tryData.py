import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('..')
import util.db as db
import util.plot as plot
import pprint

data = ['EWZS']

df = pd.DataFrame(data)

my_judge = [];
for i in range(df.shape[0]):
    # print df[i]
    ticker = df.loc[i]
    print ticker,'========================='
    ticker_id = ticker[0]
    plot.plotCurrentMeanStd(ticker_id,400)
    ticker_judge = raw_input()#1:buy,0:no,2:interest
    my_judge.append((ticker_id,ticker_judge))




pprint.pprint(my_judge)


