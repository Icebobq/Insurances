import requests
import queue
import re
import datetime
from requests.packages import urllib3
urllib3.disable_warnings()
#健康优选版
url = 'https://www.baodan360.com/insurance/detail/id/133656/'
Sex = ['男', '女']
Extra = ['含附加被保人豁免','不含附加被保人豁免']
Insurance_Period = ['保20年','保30年','至60周岁','至70周岁','保10年']
Pay_Period = ['1','5','10', '20','30']
Insurance_Amount = [x * 10 for x in range(3, 21)]
First_City = [110100,310100,440100,440300,320500,330200,330100,320100]
Second_City = [110100,310100,120100,500100,230100,220100,210100,150100,130100,
            650100,620100,630100,610100,640100,410100,370100,140100,340100,
            420100,430100,320100,510100,520100,530100,450100,330100,
            360100,440100,350100,710000,810000,820000,460100,
               150200,210200,220200,230600,410300,420500,430700,450200,510700,520300,340200,
               130200,130600,130900,350200,350500,350600,330300,330400,330600,330700,331000,
               440400,440600,440700,440800,440900,441300,441900,442000,371600,371700,
               370200,370300,370500,370600,370700,370800,370900,371000,371300,371400,371500,
               320200,320300,320400,320600,320800,320900,321000,321100,321200]
RESULTS = []
dictionary_standard = {}
dictionary_healthy = {}
dictionary_extra = {}
try:
    response = requests.get(url,verify=False)
    content = response.text
    try:
        pattern = re.compile('g_price_rule.*?{"rule":(.*?)},"5979".*?{"rule":(.*?)}};', re.S)
        items = re.findall(pattern, str(content))
        dictionary_standard = eval(items[0][0])
        dictionary_healthy = eval(items[0][1])
        pattern = re.compile('g_price_rule.*?"1229".*?{"rule":(.*?)}},"5979"', re.S)
        items = re.findall(pattern, str(content))
        dictionary_extra = eval(items[0])
    except:
        print(u"系统：访问投保链接失败！")
        RESULTS.append(["系统：访问投保链接失败！"])
except:
    print(u"系统：无法访问投保链接！")
    RESULTS.append(["系统：无法访问投保链接！"])

def information(Year,Sex,Insper,Payper,Insamo,extra):
    if Sex == "男": Sex = "M"
    else: Sex = "F"
    Header = str(Sex) + '_'
    if Insper == "保20年":
        Insper = 'A20'
    elif Insper == "保30年":
        Insper = 'A30'
    elif Insper == "至70周岁":
        Insper = 'B70'
    elif Insper == "至60周岁":
        Insper = 'B60'
    else:
        Insper = 'A10'
    Header = Header + str(Insper) + '_' + str(Payper) + '_' + str(datetime.datetime.now().year - Year)

    Results = []
    try:
        if extra == "含附加被保人豁免":
            Price = float(dictionary_healthy[Header]) * int(Insamo) * 10
            Price = Price + Price / 1000 * float(dictionary_extra[Header])
        else:
            Price = float(dictionary_healthy[Header]) * int(Insamo) * 10
        Results.append(str(round(Price,2)))
        return Results
    except:
        return None

def start(Address,Year,Sex,minInsamo,maxInsamo,self_Insper,self_Payper,self_Smoke,self_Healthy,self_SIN,Address_SIN,self_BMI,self_Job):
    if RESULTS != []:
        return RESULTS
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS

    if datetime.datetime.now().year - int(Year) <= 40:
        if int(Address[0][1]) in First_City:
            if maxInsamo > 200: maxInsamo = 200
        elif int(Address[0][1]) in Second_City:
            if maxInsamo > 150: maxInsamo = 150
        else:
            if maxInsamo > 100: maxInsamo = 100
    else:
        if int(Address[0][1]) in First_City:
            if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Second_City:
            if maxInsamo > 60: maxInsamo = 60
        else:
            if maxInsamo > 50: maxInsamo = 50

    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        for Payper in Pay_Period:
            if self_Payper != -1:
                if self_Payper not in Pay_Period: return (["系统:不提供该指定交费期间！"])
                if int(Payper) != int(self_Payper): continue
            for Insper in Insurance_Period:
                if self_Insper != "无":
                    if self_Insper not in Insurance_Period: return (["系统:不提供该指定保障期间！"])
                    if Insper != self_Insper: continue
                if Insper == "保20年":
                    timee = 20
                elif Insper == "保30年":
                    timee = 30
                elif Insper == "至70周岁":
                    timee = 70 - datetime.datetime.now().year + Year
                elif Insper == "至60周岁":
                    timee = 60 - datetime.datetime.now().year + Year
                else:
                    timee = 10
                if int(Payper) > timee: continue
                if datetime.datetime.now().year - int(Year) >= 40:
                    if Insper == "至70周岁": continue
                if datetime.datetime.now().year - int(Year) > 30:
                    if datetime.datetime.now().year - int(Year) <= 49:
                        if Insper == "至60周岁":
                            if int(Payper) == 30: continue
                if datetime.datetime.now().year - int(Year) > 40:
                    if Insper == "保30年" or Insper == "至70周岁":
                        if int(Payper) == 30: continue
                    elif Insper == "至60周岁":
                        if int(Payper) == 20 or int(Payper) == 30: continue
                for extra in Extra:
                    if int(Payper) == 1 and extra == "含附加被保人豁免": continue
                    items = information(Year, Sex, Insper, Payper, Insamo, extra)
                    if items:
                        RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                                       str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(extra) + "," + str(items[0]))
                        print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                              str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(extra) + "," + str(items[0]))

    return RESULTS