import requests
import queue
import datetime
import re
import json
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "https://api.iyb.tm/sale/perform.json?_version=2.5&_client=2"
data = {'accountId': "500945465",
        'content': {'AMOUNT': "100000",
                    'BIRTHDAY': "1995-02-06",
                    'EFFECTIVE_DATE': "today",
                    'GENDER': "F",
                    'INSURE': "term_30",
                    'PAY': "term_20",
                    'ZONE': {'label': "龙岗区",
                            'value': "440307",
                            'parents': [{'label': "广东省", 'value': "440000"}, {'label': "深圳市", 'value': "440300"}]},
                    'packId': 96},
        'inviteChannel': "ios-share-wechat-session",
        'opt': "try",
        'platformId': 2,
        'productId': "1030018",
        'shareType': "list",
        'time': "1537364803234",
        'wareId': "60"}
header = {'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://sky.zhongan.com',
            'Referer': 'https://sky.zhongan.com/m/short/trial?wareId=60&productId=1030018&accountId=500945465&shareType=list&inviteChannel=ios-share-wechat-session&time=1537364803234',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
Sex = ['男', '女']
Insurance_Period = ['保20年', '保30年']
Pay_Period = ['10', '20']
Insurance_Amount = [x * 10 for x in range(1, 16)]
Main_Pro = [350000,310000,420000,440000,110000,340000,510000,370000,450000,
            330000,320000,120000,210000,130000,140000,410000,150000,220000,
            230000,360000,430000,460000,500000,520000,530000,610000,620000,
            630000,640000,650000]
RESULTS = []

def contractWeb():
    try:
        response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo):
    data["content"]["BIRTHDAY"] = str(Year)+"-01-01"
    data["content"]['PAY'] = "term_"+str(Payper)

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["content"]['GENDER'] = str(Sex)

    if Insper == "保20年": Insper = "term_20"
    else: Insper = "term_30"
    data["content"]['INSURE'] = str(Insper)

    ins_amount = int(Insamo)*10000
    data["content"]['AMOUNT'] = str(ins_amount)

    content = contractWeb()
    if not content:
        time.sleep(1)
        content = contractWeb()
    if not content:
        print(u"系统：无法访问投保链接！")
        return None

    Results = []
    pattern = re.compile('"rules":\[(.*?)\]}', re.S)
    items = re.findall(pattern, str(content))
    Results.append(items)
    pattern = re.compile('"total":(.*?),', re.S)
    items = re.findall(pattern, str(content))
    #if str(items).find("-1") == -1:
    try:
        Results.append(items[0].strip())
        return Results
    except:
        print(u"系统：访问投保链接失败！")
        return None

def start(Address,Year,Sex,minInsamo,maxInsamo,self_Insper,self_Payper,self_Smoke,self_Healthy,self_SIN,Address_SIN,self_BMI,self_Job):
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if int(Address[0][0]) not in Main_Pro:
        print("系统：该产品不允许该客户的所在地区投保！")
        return(["系统：该产品不允许该客户的所在地区投保！"])
    else:
        data["content"]['ZONE']['value'] = str(Address[0][2])
        data["content"]['ZONE']['label'] = str(Address[1][2])
        data["content"]['ZONE']['parents'][0]['value'] = str(Address[0][0])
        data["content"]['ZONE']['parents'][0]['label'] = str(Address[1][0])
        data["content"]['ZONE']['parents'][1]['value'] = str(Address[0][1])
        data["content"]['ZONE']['parents'][1]['label'] = str(Address[1][1])
    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        #if datetime.datetime.now().year - Year > 45 and int(Insamo) > 60: break
        for Payper in Pay_Period:
            if self_Payper != -1:
                if self_Payper not in Pay_Period:
                    print("系统:不提供该指定交费期间！")
                    return(["系统:不提供该指定交费期间！"])
                if int(Payper) != int(self_Payper): continue
            for Insper in Insurance_Period:
                if self_Insper != "无":
                    if self_Insper not in Insurance_Period:
                        print("系统:不提供该指定保障期间！")
                        return (["系统:不提供该指定保障期间！"])
                    if Insper != self_Insper: continue
                if datetime.datetime.now().year - Year <= 25 and Insper == "保20年": continue
                if Insper == "保20年": timee = 20
                else: timee = 30
                if int(Payper) > timee: continue
                items = information(Year, Sex, Insper, Payper, Insamo)
                if items:
                    RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + str(items[1]) + "," + str(items[0]))
                    print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[1]) + "," + str(items[0]))
    return RESULTS