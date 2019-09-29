import requests
import queue
import datetime
import re
import json
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "http://weixin.hongkang-life.com/hk/dqLife2019/do/quote"
data = {'age': '23',
        'amnt': "10",
        'areaCode': "110000",
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
            'Cookie': 'OZ_1U_2863=vid=vbe5eeb794d9b9.0&ctime=1542327849&ltime=1542327835; Hm_lvt_95a9bc943e08216049a25e5774291ef8=1542327773,1544672790,1544751206,1544751656; Hm_lpvt_95a9bc943e08216049a25e5774291ef8=1544751656; SERVERID=0d714961e7636c51c328919eccd0aec7|1544751749|1544751517',
            'Host': 'weixin.hongkang-life.com',
            'Origin': 'http://weixin.hongkang-life.com',
            'Referer': 'http://weixin.hongkang-life.com/View/page/dqLife2019/product.html?sr=ygb3942&user_id=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
Sex = ['男', '女']
Insurance_Period = ['保20年', '保30年', '至60周岁', '至70周岁']
Pay_Period = ['1','5','10', '20', '30','至60周岁', '至70周岁']
Insurance_Amount = [x * 10 for x in range(1, 16)]
First_City = [110100,310100,440100,440300,
              120100, 500100, 230100, 220100, 210100, 150100, 130100,
              650100, 620100, 630100, 610100, 640100, 410100, 370100, 140100, 340100,
              420100, 430100, 320100, 510100, 520100, 530100, 450100, 540100, 330100,
              360100, 350100, 710000, 810000, 820000, 460100,
              370200, 210200, 330200, 350200, 441900, 440600, 320400, 320600, 320500,
              320200, 150200]
Second_City = [340800, 340300, 341200, 350800, 350300, 350500, 350400, 350600,
               442000, 440400, 450500, 450300, 520300, 130800, 130300, 130200,
               410200, 410300, 230600, 420200, 420600, 430700, 430600, 430200,
               320800, 320700, 321200, 321300, 320300, 320900, 321000, 321100,
               361000, 360700, 360200, 360400, 360300, 210300, 150400, 640200,
               370500, 370600, 370300, 140200, 610400, 610800, 510600, 511100, 510500,
               650200, 530300, 530400, 330500, 330400, 330700, 330600, 331000, 330300, 330900]
Jobs = ['1','2','3','4','5','6']
RESULTS = []

def contractWeb():
    try:
        response = requests.post(url,data=json.dumps(data),headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Sex, Insper,Payper,Insamo):
    if Sex == '男':
        data['sex'] = '0'
    else:
        data['sex'] = '1'

    if Insper == "至60周岁":
        data['insuyear'] = '60'
        data['insuyearflag'] = 'A'
    elif Insper == "保20年":
        data['insuyear'] = '20'
        data['insuyearflag'] = 'Y'
    elif Insper == "保30年":
        data['insuyear'] = '30'
        data['insuyearflag'] = 'Y'
    else:
        data['insuyear'] = '70'
        data['insuyearflag'] = 'A'

    if Payper == "至60周岁":
        data['payendyear'] = '60'
        data['payendyearflag'] = 'A'
    elif Payper == "至70周岁":
        data['payendyear'] = '70'
        data['payendyearflag'] = 'A'
    else:
        data['payendyear'] = str(Payper)
        data['payendyearflag'] = 'Y'

    data['amnt'] = str(Insamo)

    content = contractWeb()
    if not content:
        time.sleep(1)
        content = contractWeb()
    if not content:
        print(u"系统：无法访问投保链接！")
        return None

    Results = []

    pattern = re.compile('"msg":"(.*?)"}', re.S)
    items = re.findall(pattern, str(content))
    Results.append(items)

    pattern = re.compile('"prem":(.*?),', re.S)
    items = re.findall(pattern, str(content))
    try:
        Results.append(items[0].strip())
        return Results
    except:
        return None

def start(Address,Year,Sex,self_salary,minInsamo,maxInsamo,self_Insper,self_Payper,self_Smoke,self_height,self_weight,self_Job):
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 20:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if self_Job[2] not in Jobs:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    else:
        if str(self_Job[2]) == '5' or str(self_Job[2]) == '6':
            if maxInsamo > 50:
                maxInsamo = 50
        if self_salary < 10:
            if maxInsamo > 70:
                maxInsamo = 70

    data['age'] = str(datetime.datetime.now().year - Year)
    data['height'] = str(self_height)
    data['weight'] = str(self_weight)

    if self_Smoke == '不吸烟':
        data['smoking'] = '1'
    elif self_Smoke == '每天小于10支':
        data['smoking'] = '2'
    elif self_Smoke == '每天10-20支':
        data['smoking'] = '3'
    else:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS

    if str(Address[1][1]) == '市辖区':
        data['areaCode'] = str(Address[0][0])
    else:
        data['areaCode'] = str(Address[0][1])

    if datetime.datetime.now().year - Year <= 40:
        if int(Address[0][1]) in First_City:
            if maxInsamo > 150: maxInsamo = 150
        elif int(Address[0][1]) in Second_City:
            if maxInsamo > 100: maxInsamo = 100
        else:
            if maxInsamo > 50: maxInsamo = 50
    else:
        if int(Address[0][1]) in First_City:
            if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Second_City:
            if maxInsamo > 80: maxInsamo = 80
        else:
            if maxInsamo > 50: maxInsamo = 50

    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        for Payper in Pay_Period:
            if self_Payper != -1:
                if self_Payper not in Pay_Period: return(["系统:不提供该指定交费期间！"])
                if str(Payper) != str(self_Payper): continue
            if Payper == '30' or Payper == '至60周岁':
                if datetime.datetime.now().year - Year > 40: continue
            for Insper in Insurance_Period:
                if self_Insper != "无":
                    if self_Insper not in Insurance_Period: return (["系统:不提供该指定保障期间！"])
                    if Insper != self_Insper: continue
                if Insper == "至70周岁": timee = 70 - datetime.datetime.now().year + Year
                elif Insper == "保20年": timee = 20
                elif Insper == "保30年": timee = 30
                else: timee = 60 - datetime.datetime.now().year + Year
                if Payper == '至60周岁':
                    if 60 - datetime.datetime.now().year + Year > timee: continue
                elif Payper == '至70周岁':
                    if 70 - datetime.datetime.now().year + Year > timee: continue
                else:
                    if int(Payper) > timee: continue
                items = information(Sex, Insper, Payper, Insamo)
                if items:
                    RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + str(items[1]) + "," + str(items[0]))
                    print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[1]) + "," + str(items[0]))
    return RESULTS

age = 23
sex = '男'
Insamo = 12
minInsamo = 60
maxInsamo = 120
Insper = '保30年'
Payper = -1
Smoke = '不吸烟'
height = 162
weight = 44
address = [[110000, 110100, 110000], ['北京市', '市辖区', '龙岗区']]
Job = [['013', '01301', '0013102'], ['文教机关', '教育机构', '学生'], '1']

Results = start(address, datetime.datetime.now().year - int(age),
                                  sex, int(Insamo), minInsamo, maxInsamo, Insper, Payper,
                                  Smoke, height, weight, Job)
print(Results)