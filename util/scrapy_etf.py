import requests
import simplejson as json
import pandas as pd

# url = 'https://xueqiu.com/hq#exchange=US&plate=3_1_11&firstName=3&secondName=3_1&order=desc&orderby=marketcapital&page=1'
url1 = 'https://xueqiu.com/snowman/login'

data = {
    "remember_me":"true",
    "username":"13151998870",
    "password":"zhangyizhi112358"
}
headers = { 
"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Host":"xueqiu.com",
"Pragma":"no-cache",
"Referer":"https://xueqiu.com/hq",
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",
}

res1 = requests.post(url1,data,headers=headers)

target_data = []
pageNum = 1

while True:
    url2 = 'http://xueqiu.com/stock/cata/stocklist.json?page=%s&size=30&order=desc&orderby=marketCapital&exchange=US&plate=ETF&isdelay=1' % (pageNum)
    res2 = requests.get(url2, cookies=res1.cookies, headers=headers)
    stock_data = json.loads(res2.text)['stocks']



    print 'pageNum: ', pageNum ,' ====================================='

    # print stock_data,'---------------------------'



    if len(stock_data) == 0 :
        break

    for i in range(len(stock_data)):
        stock = stock_data[i]
        stock_id = stock['code'].encode('utf-8')
        stock_name = stock['name'].encode('utf-8')
        print stock_id,stock_name
        target_data.append((stock_id,stock_name))

    pageNum = pageNum + 1

   

df = pd.DataFrame(target_data,columns=['Symbol','Name'])
df.to_csv('etf.csv')



print target_data

