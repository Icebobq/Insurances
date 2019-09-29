import requests
import queue
import datetime
import re
import json
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "https://api.iyb.tm/sale/perform.json?_version=2.5&_client=2&__MYLOG_UID=d2ab7766-b615-49e2-9ec1-2f85709c40c8&__MYLOG_SID=aa87b3fe-2431-4940-a77c-75e10796acd8"
data = {'accountId': "500945465",
        'content': {
                    'AMOUNT': "1000000",
                    'BIRTHDAY': "1990-01-01",
                    'GENDER': "M",
                    'INSURE': "to_70",
                    'PAY': "term_20",
                    'SOCIAL_INS': "Y",
                    'packId': '20014'},
        'opt': "try",
        'platformId': '2',
        'productId': "1032249",
        'wareId': "20014"}
header = {'accept': 'application/json',
            'content-type': 'application/json',
            'Origin': 'https://sky.iyunbao.com',
            'Referer': 'https://sky.iyunbao.com/m/short/trial?wareId=20014&productId=1032249&accountId=500945465',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
Sex = ['男', '女']
SocialSecurity = ['有社保','无社保']
Insurance_Period = ['保10年', '保20年', '保30年', '至60周岁', '至65周岁', '至70周岁']
Pay_Period = ['1','5','10', '20', '30']
Insurance_Amount = [x * 10 for x in range(1, 31)]
# 北京、上海、广州、深圳、苏州、宁波、杭州、南京、武汉、成都
First_City = [110100,310100,440100,440300,320500,330200,330100,320100,420100,510100]
Second_City = [110100,310100,120100,500100,230100,220100,210100,150100,130100,
            650100,620100,630100,610100,640100,410100,370100,140100,340100,
            420100,430100,320100,510100,520100,530100,450100,330100,
            360100,440100,350100,710000,810000,820000,460100,
               150200,210200,220200,230600,410300,420500,430700,450200,510700,520300,340200,
               130200,130600,130900,350200,350500,350600,330300,330400,330600,330700,331000,
               440400,440600,440700,440800,440900,441300,441900,442000,371600,371700,
               370200,370300,370500,370600,370700,370800,370900,371000,371300,371400]
Jobs = ['1','2','3','4','5','6']
RESULTS = []

def contractWeb():
    try:
        response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo,SIN):
    data["content"]["BIRTHDAY"] = str(Year)+"-01-01"
    data["content"]['PAY'] = "term_"+str(Payper)

    if SIN == "有社保": SIN = "Y"
    else: SIN = "N"
    data["content"]['SOCIAL_INS'] = str(SIN)

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["content"]['GENDER'] = str(Sex)

    if Insper == "至70周岁": Insper = "to_70"
    elif Insper == "至65周岁": Insper = "to_65"
    elif Insper == "保20年": Insper = "term_20"
    elif Insper == "保30年": Insper = "term_30"
    elif Insper == "保10年": Insper = "term_10"
    else: Insper = "to_60"
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
    if self_Job[2] not in Jobs:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if datetime.datetime.now().year - Year > 60 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    for SIN in SocialSecurity:
        if self_SIN != "不提供":
            if SIN != self_SIN: continue
        if SIN == "有社保":
            if datetime.datetime.now().year - Year <= 40:
                if int(Address_SIN[0][1]) in First_City:
                    if maxInsamo > 300: maxInsamo = 300
                elif int(Address_SIN[0][1]) in Second_City:
                    if maxInsamo > 200: maxInsamo = 200
                else:
                    if maxInsamo > 150: maxInsamo = 150
            elif datetime.datetime.now().year - Year <= 50:
                if int(Address_SIN[0][1]) in First_City:
                    if maxInsamo > 200: maxInsamo = 200
                elif int(Address_SIN[0][1]) in Second_City:
                    if maxInsamo > 150: maxInsamo = 150
                else:
                    if maxInsamo > 100: maxInsamo = 100
            else:
                if int(Address[0][1]) in First_City:
                    if maxInsamo > 100: maxInsamo = 100
                elif int(Address[0][1]) in Second_City:
                    if maxInsamo > 80: maxInsamo = 80
                else:
                    if maxInsamo > 50: maxInsamo = 50
        else:
            if datetime.datetime.now().year - Year <= 40:
                if int(Address[0][1]) in First_City:
                    if maxInsamo > 200: maxInsamo = 200
                elif int(Address[0][1]) in Second_City:
                    if maxInsamo > 150: maxInsamo = 150
                else:
                    if maxInsamo > 100: maxInsamo = 100
            elif datetime.datetime.now().year - Year <= 50:
                if int(Address[0][1]) in First_City:
                    if maxInsamo > 150: maxInsamo = 150
                elif int(Address[0][1]) in Second_City:
                    if maxInsamo > 100: maxInsamo = 100
                else:
                    if maxInsamo > 50: maxInsamo = 50
            else:
                if int(Address[0][1]) in First_City:
                    if maxInsamo > 80: maxInsamo = 80
                elif int(Address[0][1]) in Second_City:
                    if maxInsamo > 50: maxInsamo = 50
                else:
                    if maxInsamo > 30: maxInsamo = 30
        for Insamo in Insurance_Amount:
            if int(Insamo) < minInsamo: continue
            if int(Insamo) > maxInsamo: break
            if int(Insamo) <= 200:
                if self_BMI < 16 or self_BMI >= 33: continue
            else:
                if self_BMI < 16 or self_BMI > 30: continue
            for Payper in Pay_Period:
                if self_Payper != -1:
                    if self_Payper not in Pay_Period: return(["系统:不提供该指定交费期间！"])
                    if int(Payper) != int(self_Payper): continue
                for Insper in Insurance_Period:
                    if self_Insper != "无":
                        if self_Insper not in Insurance_Period: return (["系统:不提供该指定保障期间！"])
                        if Insper != self_Insper: continue
                    if Insper == "至70周岁": timee = 70 - datetime.datetime.now().year + Year
                    elif Insper == "保20年": timee = 20
                    elif Insper == "保30年": timee = 30
                    elif Insper == "保10年": timee = 10
                    elif Insper == "至65周岁":
                        timee = 65 - datetime.datetime.now().year + Year
                    else: timee = 60 - datetime.datetime.now().year + Year
                    if int(Payper) > timee: continue
                    items = information(Year, Sex, Insper, Payper, Insamo, SIN)
                    if items:
                        RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                              str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + str(SIN) + "," + str(items[1]) + "," + str(items[0]))
                        print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                              str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(SIN) + "," + str(items[1]) + "," + str(items[0]))
    return RESULTS

# re = information(1995,'男','保30年','20','30','有社保')
# print(re)