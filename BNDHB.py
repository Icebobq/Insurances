import requests
import queue
import datetime
import re
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "http://www.kaixinbao.com/wj/shop/filter!premDoCal.action"
data = {'BTsc0050000000019190_TextAge': '40Y',
        'BTsc0050000000019191_Sex': 'M',
        'BTsc0050000000019192_Period': '30Y',
        'BTsc0050000000019193_FeeYear': '30Y',
        'BTsc0050000000019194_Plan': '1500000',
        'BTsc0050000000019196_Occup': '1-4',
        'RiskCode': '224801031',
        'complicatedFlag': 'Y',
        'channelSn': 'cps_swpt',
        'duty': '224801031001-1500000'}
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '271',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'acw_tc=76b20f4315420873487521761e627a29a9468655e4522f0b976d8033ace809; NTKF_T2D_CLIENTID=guest31F60DEE-5292-D24E-6BAD-0B9196E193C4; gr_user_id=82eca633-b4a1-4b75-8496-25acdc65ffae; grwng_uid=dca4ef56-997c-432e-8f8f-4674dc875f66; cpsUserId=105600; partners_uid=; channelSn=cps_swpt; cpstype=CPS; cpsUserSource=8_swpt; JSESSIONID=7E9207CEE227B0000EE858D7664E6EFB; vlid_1001=------QFspYTyx18592595990---------154208520015420873491543937797d--6--8--l--0--; nTalk_CACHE_DATA={uid:kf_9401_ISME9754_guest31F60DEE-5292-D2,tid:1543937797881720}; a6211e66e314d44f_gr_session_id=3521132c-09f9-4ab9-a78b-66cf975694a0; Hm_lvt_b0d61b2de58bce03e74718744c2eb82d=1542422487,1542515683,1543282365,1543937800; Hm_lpvt_b0d61b2de58bce03e74718744c2eb82d=1543937800; a6211e66e314d44f_gr_session_id_3521132c-09f9-4ab9-a78b-66cf975694a0=true',
            'Host': 'www.kaixinbao.com',
            'Origin': 'http://www.kaixinbao.com',
            'Referer': 'http://www.kaixinbao.com/renshou-baoxian/313866.shtml?CPS&cpsUserCode=105600&cpsUserSource=8_swpt',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
Sex = ['男', '女']
Insurance_Period = ['保30年','至60周岁','至65周岁','至70周岁']
Pay_Period = ['10', '20','30']
Insurance_Amount = [x * 10 for x in range(4, 16)]
Main_City = [110100,310100,440100,440300]
Pro_City = [110100,310100,120100,500100,230100,220100,210100,150100,130100,
            650100,620100,630100,610100,640100,410100,370100,140100,340100,
            420100,430100,320100,510100,520100,530100,450100,540100,330100,
            360100,440100,350100,710000,810000,820000,460100]
Plan_City = [440300,330200,370200,210200,350200]
Jobs = ['1','2','3','4']
RESULTS = []

def contractWeb():
    try:
        response = requests.post(url,data=data,headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo):
    data["BTsc0050000000019190_TextAge"] = str(datetime.datetime.now().year - Year)+"Y"
    data["BTsc0050000000019193_FeeYear"] = str(Payper)+"Y"

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["BTsc0050000000019191_Sex"] = str(Sex)

    if Insper == "保30年": Insper = "30Y"
    elif Insper == "至70周岁": Insper = "70A"
    elif Insper == "至60周岁": Insper = "60A"
    else: Insper = "65A"
    data["BTsc0050000000019192_Period"] = str(Insper)

    ins_amount = int(Insamo)*10000
    data["BTsc0050000000019194_Plan"] = str(ins_amount)

    data['duty'] = '224801031001-'+str(ins_amount)

    content = contractWeb()
    if not content:
        time.sleep(1)
        content = contractWeb()
    if not content:
        print(u"系统：无法访问投保链接！")
        return None

    Results = []
    try:
        pattern = re.compile('"status":"(.*?)"', re.S)
        items = re.findall(pattern, str(content))
        if str(items[0]) == '2':
            pattern = re.compile('"msg":"(.*?)"', re.S)
            items = re.findall(pattern, str(content))
            RESULTS.append(items[0])
            print(items[0])
            return None
        pattern = re.compile('"productPrem":"(.*?)"', re.S)
        items = re.findall(pattern, str(content))
        Results.append(items[0])
        return Results
    except:
        print(u"系统：访问投保链接失败！")
        return None

def start(Address,Year,Sex,minInsamo,maxInsamo,self_Insper,self_Payper,self_Smoke,self_Healthy,self_SIN,Address_SIN,self_BMI,self_Job):
    if self_Job[2] not in Jobs:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    if datetime.datetime.now().year - Year > 50 or datetime.datetime.now().year - Year < 25:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
# 投保年龄25-40周岁：北上广深≤150万；
# 其它直辖市、省会、计划单列市≤100万；
# 其它城市≤80万。
# 投保年龄41-50周岁：北上广深≤100万；
# 其它直辖市、省会、计划单列市≤60万；
# 其它城市≤50万
    if datetime.datetime.now().year - Year <= 40:
        if int(Address[0][1]) in Main_City:
            if maxInsamo > 150: maxInsamo = 150
        elif int(Address[0][1]) in Pro_City:
            if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Plan_City:
            if maxInsamo > 100: maxInsamo = 100
        else:
            if maxInsamo > 80: maxInsamo = 80
    else:
        if int(Address[0][1]) in Main_City:
            if maxInsamo > 100: maxInsamo = 100
        elif int(Address[0][1]) in Pro_City:
            if maxInsamo > 60: maxInsamo = 60
        elif int(Address[0][1]) in Plan_City:
            if maxInsamo > 60: maxInsamo = 60
        else:
            if maxInsamo > 50: maxInsamo = 50
    for Insamo in Insurance_Amount:
        if int(Insamo) < minInsamo: continue
        if int(Insamo) > maxInsamo: break
        for Payper in Pay_Period:
            if self_Payper != -1:
                if self_Payper not in Pay_Period: return(["系统:不提供该指定交费期间！"])
                if int(Payper) != int(self_Payper): continue
            for Insper in Insurance_Period:
                if self_Insper != "无":
                    if self_Insper not in Insurance_Period: return (["系统:不提供该指定保障期间！"])
                    if Insper != self_Insper: continue
                #if datetime.datetime.now().year - Year <= 25 and Insper == "保20年": continue
                if Insper == "保30年": timee = 30
                elif Insper == "至70周岁": timee = 70 - datetime.datetime.now().year + Year
                elif Insper == "至60周岁": timee = 60 - datetime.datetime.now().year + Year
                else: timee = 65 - datetime.datetime.now().year + Year
                if int(Payper) > timee: continue
                items = information(Year, Sex, Insper, Payper, Insamo)
                if items:
                    RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + str(items[0]))
                    print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[0]))
    return RESULTS