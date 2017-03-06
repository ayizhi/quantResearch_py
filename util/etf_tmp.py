import pandas as pd
import numpy as np
import db


data = pd.read_csv('etf.csv')

data['Sector'] = 'ETF'

data = data[['Symbol','Sector','Name']]



db.save_us_into_db(data)