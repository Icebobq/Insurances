import re
import requests
import json

url = 'http://weixin.hongkang-life.com/hk/dqLife2019/do/quote'
data = {'age': '23',
'amnt': "10",
'areaCode': "443000",
'height': "162",
'insuyear': "20",
'insuyearflag': "Y",
'occCode': "0013102",
'payendyear': "20",
'payendyearflag': "Y",
'payintv': '12',
'riskCode': "RC067",
'sex': "0",
'smoking': "1",
'weight': "44"}
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Length': '215',
'Content-Type': 'application/json;charset=UTF-8',
'Cookie': 'OZ_1U_2863=vid=vbe5eeb794d9b9.0&ctime=1542327849&ltime=1542327835; Hm_lvt_95a9bc943e08216049a25e5774291ef8=1544768955,1544770405,1544773059,1545611369; Hm_lpvt_95a9bc943e08216049a25e5774291ef8=1545612493; SERVERID=0d714961e7636c51c328919eccd0aec7|1545612516|1545611366',
'Host': 'weixin.hongkang-life.com',
'Origin': 'http://weixin.hongkang-life.com',
'Referer': 'http://weixin.hongkang-life.com/View/page/dqLife2019/product.html?sr=ygb3942&user_id=0',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}
response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
content = response.text
print(content)