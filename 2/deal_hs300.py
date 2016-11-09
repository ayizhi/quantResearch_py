# 股票价格的预测分类/回归模型
# 1. price between 10-50 
# 2. 沪深三百内的 
# 3. average daily volume (ADV) in the middle 33 percentile

import db
from db import get_10_50_by_id,get_tickers_from_db

tickers = get_tickers_from_db
print tickers
