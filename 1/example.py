import pandas as pd
df1 = pd.DataFrame([[1,2,3],[5,6,7],[3,9,0],[8,0,3]],columns=['x1','x2','x3'])
df2 = pd.DataFrame([[1,2],[4,6],[3,9]],columns=['x1','x4'])
print df1
print df2
df3 = pd.merge(df1,df2,how = 'left',on='x1')
print df3