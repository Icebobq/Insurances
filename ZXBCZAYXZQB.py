import requests
import queue
import datetime
import re
import json
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "https://api.iyb.tm/sale/perform.json"
data = {"platformId": "2",
         "opt": "try",
         "content": {"BIRTHDAY": "1999-01-01",
                     'BENEF_LEVEL': "1",
                     'BENEF_LEVEL_DESC': "最终根据免费体检结果确定费率档",
                     "GENDER": "M",
                     "AMOUNT": "60",
                     "PAY": "term_20",
                     "INSURE": "to_70",
                     "ZONE": 'null',
                     "SMOKE": "2",
                     "packId": "47",
                     "SOCIAL_ZONE": 'null',
                     "OCCUPATION_L": 'null'}
         }
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '286',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'JSESSIONID=FFB640AFA8341BC605D0E3E6777670BD',
            'Host': 'api.iyb.tm',
            'Origin': 'https://sv.iyb.tm',
            'Referer': 'https://sv.iyb.tm/iyb/ware.mobile?wareId=30&productId=1028756&accountId=500945465&shareType=list&inviteChannel=ios-share-wechat-session&time=1541664614894&from=singlemessage&isappinstalled=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
Sex = ['男', '女']
Extra = ['吸烟', '不吸烟']
Insurance_Period = ['保20年', '保30年', '至60周岁', '至70周岁']
Pay_Period = ['10', '20', '30']
Health = ['标准体','优选体','超优体']
Insurance_Amount = [x * 10 for x in range(4, 251)]
Main_city = [110100,310100,440100,440300,420100,510100,320100,410100,320500]

def contractWeb():
    try:
        response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo,Smoke,Health):
    data["content"]["BIRTHDAY"] = str(Year) + "-01-01"
    data["content"]['PAY'] = "term_" + str(Payper)
    data["content"]['AMOUNT'] = str(Insamo)

    if Smoke == "吸烟": Smoke = "1"
    else: Smoke = "2"
    data["content"]['SMOKE'] = str(Smoke)

    if Health == "标准体": Health = "1"
    elif Health == "优选体": Health = "2"
    else: Health = "3"
    data["content"]['BENEF_LEVEL'] = str(Health)

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["content"]['GENDER'] = str(Sex)

    if Insper == "至70周岁": Insper = "to_70"
    elif Insper == "保20年": Insper = "term_20"
    elif Insper == "保30年": Insper = "term_30"
    else: Insper = "to_60"
    data["content"]['INSURE'] = str(Insper)

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
    RESULTS = []
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if int(Address[0][1]) not in Main_city:
        return(["系统：该产品不允许该客户的所在地区投保！"])
    else:
        data["content"]['ZONE'] = str(Address[0][1])
        if int(Address[0][1]) != 320500:
            if datetime.datetime.now().year - Year > 45:
                if minInsamo < 70: minInsamo = 70
            else:
                if minInsamo < 110: minInsamo = 110
        else:
            if datetime.datetime.now().year - Year > 45:
                if minInsamo < 40: minInsamo = 40
            else:
                if minInsamo < 60: minInsamo = 60
    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        for Payper in Pay_Period:
            if Payper == "30" and datetime.datetime.now().year - Year > 40: break
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
                else: timee = 60 - datetime.datetime.now().year + Year
                if Insper == "保20年" and Payper != "20": continue
                if Insper == "保30年" and Payper != "30": continue
                if int(Payper) > timee: continue
                for Smoke in Extra:
                    if self_Smoke != "不提供":
                        if Smoke != self_Smoke: continue
                    for Healthy in Health:
                        if self_Healthy != "不提供":
                            if Healthy != self_Healthy: continue
                        items = information(Year, Sex, Insper, Payper, Insamo, Smoke, Healthy)
                        if items:
                            RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                                  str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + Smoke + "," + Healthy + "," +
                                  str(items[1]) + "," + str(items[0]))
                            print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                                  str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + Smoke + "," + Healthy + "," +
                                  str(items[1]) + "," + str(items[0]))
    return RESULTS