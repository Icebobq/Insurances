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
                     "GENDER": "M",
                     "AMOUNT": "600000",
                     "PAY": "term_20",
                     "INSURE": "to_70",
                     "ZONE": 'null',
                     "SMOKE": "2",
                     "packId": "25",
                     "SOCIAL_ZONE": 'null',
                     "OCCUPATION_L": 'null'}
         }
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '201',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'JSESSIONID=E67E6CA8AAA424D84CB48F678A06D004',
            'Host': 'api.iyb.tm',
            'Origin': 'https://sv.iyb.tm',
            'Referer': 'https://sv.iyb.tm/iyb/ware.mobile?wareId=15&productId=1019133&accountId=500945465&shareType=list&inviteChannel=ios-share-wechat-',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
Sex = ['男', '女']
Extra = ['吸烟', '不吸烟']
Insurance_Period = ['保20年', '保30年', '至60周岁', '至70周岁']
Pay_Period = ['10', '20', '30']
Insurance_Amount = ['30', '40', '50', '60', '70', '80', '90', '100']
Main_City = [110100,310100,440100,440300]
Pro_City = [110100,310100,120100,500100,230100,220100,210100,150100,130100,
            650100,620100,630100,610100,640100,410100,370100,140100,340100,
            420100,430100,320100,510100,520100,530100,450100,540100,330100,
            360100,440100,350100,710000,810000,820000,460100]
Main_Pro = [350000,310000,420000,440000,110000,340000,510000,370000,450000,
            330000,320000,120000,210000,130000,140000,410000]


def contractWeb():
    try:
        response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo,Smoke):
    data["content"]["BIRTHDAY"] = str(Year)+"-01-01"
    data["content"]['PAY'] = "term_"+str(Payper)

    if Smoke == "吸烟": Smoke = "1"
    else: Smoke = "2"
    data["content"]['SMOKE'] = str(Smoke)

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["content"]['GENDER'] = str(Sex)

    if Insper == "至70周岁": Insper = "to_70"
    elif Insper == "保20年": Insper = "term_20"
    elif Insper == "保30年": Insper = "term_30"
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
    RESULTS = []
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if int(Address[0][0]) not in Main_Pro:
        data["content"]['ZONE'] = "999000"
        if datetime.datetime.now().year - Year > 45:
            if maxInsamo > 30: maxInsamo = 30
        else:
            if maxInsamo > 50: maxInsamo = 50
    else:
        data["content"]['ZONE'] = str(Address[0][1])
        if int(Address[0][1]) in Main_City:
            if datetime.datetime.now().year - Year > 45:
                if maxInsamo > 60: maxInsamo = 60
            else:
                if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Pro_City:
            if datetime.datetime.now().year - Year > 45:
                if maxInsamo > 40: maxInsamo = 40
            else:
                if maxInsamo > 80: maxInsamo = 80
        else:
            if datetime.datetime.now().year - Year > 45:
                if maxInsamo > 30: maxInsamo = 30
            else:
                if maxInsamo > 50: maxInsamo = 50
    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        if datetime.datetime.now().year - Year > 45 and int(Insamo) > 60: break
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
                    items = information(Year, Sex, Insper, Payper, Insamo, Smoke)
                    if items:
                        RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                              str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + Smoke + "," + str(items[1]) + "," + str(items[0]))
                        print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                              str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + Smoke + "," + str(items[1]) + "," + str(items[0]))
    return RESULTS