import requests

url = 'https://xueqiu.com/hq#exchange=US&plate=3_1_11&firstName=3&secondName=3_1&order=desc&orderby=marketcapital&page=1'

res = requests.get(url)

print res