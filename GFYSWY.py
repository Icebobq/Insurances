import requests
import queue
import re
import datetime
from requests.packages import urllib3
urllib3.disable_warnings()

url = 'https://www.baodan360.com/insurance/detail/id/133346'
Sex = ['男', '女']
Insurance_Period = ['保20年','保30年','至60周岁','至70周岁','至88周岁']
Pay_Period = ['10', '20','30']
Insurance_Amount = [x * 10 for x in range(1, 16)]
Main_Pro = [320000,330000,440000,350000]
Main_City = [110100,310100,120100,500100,230100,220100,210100,150100,130100,
            610100,640100,410100,370100,140100,340100,370200,
            420100,430100,510100,520100,530100,450100,440300,210200,
            360100,440100,460100]
RESULTS = []
dictionary = {}
try:
    response = requests.get(url,verify=False)
    content = response.text
    try:
        pattern = re.compile('g_price_rule.*?{"rule":(.*?)}};', re.S)
        items = re.findall(pattern, str(content))
        dictionary = eval(items[0])
    except:
        print(u"系统：访问投保链接失败！")
        RESULTS.append(["系统：访问投保链接失败！"])
except:
    print(u"系统：无法访问投保链接！")
    RESULTS.append(["系统：无法访问投保链接！"])

def information(Year,Sex,Insper,Payper,Insamo):
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
        Insper = 'B88'
    Header = Header + str(Insper) + '_' + str(Payper) + '_' + str(datetime.datetime.now().year - Year)

    Results = []
    try:
        Price = float(dictionary[str(Header)]) * int(Insamo) * 10
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
# 投保年龄18-45周岁：Main_City and Main_Pro≤100万；
# 其它城市≤80万。
# 投保年龄46-50周岁：Main_City and Main_Pro≤80万；
# 其它城市≤50万
    if datetime.datetime.now().year - int(Year) <= 40:
        if int(Address[0][0]) in Main_Pro:
            if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Main_City:
            if maxInsamo > 100: maxInsamo = 100
        else:
            if maxInsamo > 80: maxInsamo = 80
    else:
        if int(Address[0][0]) in Main_Pro:
            if maxInsamo > 80: maxInsamo = 80
        elif int(Address[0][1]) in Main_City:
            if maxInsamo > 80: maxInsamo = 80
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
                    timee = 88 - datetime.datetime.now().year + Year
                if int(Payper) > timee: continue
                if datetime.datetime.now().year - int(Year) > 40 and Insper == "至60周岁":
                    if int(Payper) == 20 or int(Payper) == 30: continue
                if datetime.datetime.now().year - int(Year) > 40:
                    if int(Payper) == 30: continue
                if datetime.datetime.now().year - int(Year) > 30 and Insper == "至60周岁":
                    if int(Payper) == 30: continue
                items = information(Year, Sex, Insper, Payper, Insamo)
                if items:
                    RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                                   str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[0]))
                    print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[0]))
    return RESULTS