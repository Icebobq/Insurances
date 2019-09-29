import requests
import queue
import datetime
import re
import time
from requests.packages import urllib3
urllib3.disable_warnings()

url = "http://www.kaixinbao.com/wj/shop/filter!premDoCal.action"
data = {'B0000000000000007402_TextAge': '40Y',
        'B0000000000000007403_Sex': 'M',
        'B0000000000000007404_Period': '30Y',
        'B0000000000000007405_FeeYear': '20Y',
        'B0000000000000007406_Plan': '1500000',
        'RiskCode': '103601005',
        'complicatedFlag': 'Y',
        'channelSn': 'cps_swpt',
        'duty': '103601005001-1500000'}
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '238',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'acw_tc=76b20f4315420873487521761e627a29a9468655e4522f0b976d8033ace809; NTKF_T2D_CLIENTID=guest31F60DEE-5292-D24E-6BAD-0B9196E193C4; gr_user_id=82eca633-b4a1-4b75-8496-25acdc65ffae; grwng_uid=dca4ef56-997c-432e-8f8f-4674dc875f66; cpsUserId=105600; partners_uid=; channelSn=cps_swpt; cpstype=CPS; cpsUserSource=8_swpt; JSESSIONID=7E9207CEE227B0000EE858D7664E6EFB; nTalk_CACHE_DATA={uid:kf_9401_ISME9754_guest31F60DEE-5292-D2,tid:1543937797881720}; a6211e66e314d44f_gr_session_id=3521132c-09f9-4ab9-a78b-66cf975694a0; Hm_lvt_b0d61b2de58bce03e74718744c2eb82d=1542422487,1542515683,1543282365,1543937800; a6211e66e314d44f_gr_session_id_3521132c-09f9-4ab9-a78b-66cf975694a0=true; vlid_1001=------QFspYTyx18592595990---------154208520015420873491543941480e--6--8--n--0--; Hm_lpvt_b0d61b2de58bce03e74718744c2eb82d=1543941482',
            'Host': 'www.kaixinbao.com',
            'Origin': 'http://www.kaixinbao.com',
            'Referer': 'http://www.kaixinbao.com/renshou-baoxian/307418.shtml?CPS&cpsUserCode=105600&cpsUserSource=8_swpt',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
Sex = ['男', '女']
Insurance_Period = ['保20年','保30年','至60周岁','至80周岁','至70周岁',
                    '至66周岁','至77周岁','至88周岁']
Pay_Period = ['1','3','5','10', '20']
Insurance_Amount = [x * 10 for x in range(1, 16)]
Main_City = [110100,310100,440100,440300]
Main_Pro = [320000,330000]
RESULTS = []

def contractWeb():
    try:
        response = requests.post(url,data=data,headers=header,verify=False)
        content = response.text
        return content
    except:
        return None

def information(Year,Sex,Insper,Payper,Insamo):
    data["B0000000000000007402_TextAge"] = str(datetime.datetime.now().year - Year)+"Y"
    data["B0000000000000007405_FeeYear"] = str(Payper)+"Y"
    if str(Payper) == '1':
        data["B0000000000000007405_FeeYear"] = '0C'

    if Sex == "男": Sex = "M"
    else: Sex = "F"
    data["B0000000000000007403_Sex"] = str(Sex)

    if Insper == "保30年": Insper = "30Y"
    elif Insper == "保20年": Insper = "20Y"
    elif Insper == "至70周岁": Insper = "70A"
    elif Insper == "至80周岁": Insper = "80A"
    elif Insper == "至60周岁": Insper = "60A"
    elif Insper == "至66周岁": Insper = "66A"
    elif Insper == "至77周岁": Insper = "77A"
    else: Insper = "88A"
    data["B0000000000000007404_Period"] = str(Insper)

    ins_amount = int(Insamo)*10000
    data["B0000000000000007406_Plan"] = str(ins_amount)

    data['duty'] = '103601005001-'+str(ins_amount)

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
    if datetime.datetime.now().year - Year > 55 or datetime.datetime.now().year - Year < 18:
        print(u"系统：该产品不适用该客户！")
        RESULTS.append(u"系统：该产品不适用该客户！")
        return RESULTS
    # 投保年龄18-40周岁：北上广深浙江江苏≤150万；
    # 其它城市≤50万。
    # 投保年龄41-50周岁：北上广深浙江江苏≤100万；
    # 其它城市≤50万
    # 投保年龄51-55周岁：北上广深浙江江苏≤50万；
    # 其它城市≤50万
    if datetime.datetime.now().year - Year <= 40:
        if int(Address[0][1]) in Main_City or int(Address[0][0]) in Main_Pro:
            if maxInsamo > 150: maxInsamo = 150
        else:
            if maxInsamo > 50: maxInsamo = 50
    elif datetime.datetime.now().year - Year <= 50:
        if int(Address[0][1]) in Main_City or int(Address[0][0]) in Main_Pro:
            if maxInsamo > 100: maxInsamo = 100
        else:
            if maxInsamo > 50: maxInsamo = 50
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
                if datetime.datetime.now().year - Year < 30 and Insper == "保30年": continue
                if Insper == "保30年": timee = 30
                elif Insper == "保20年": timee = 20
                elif Insper == "至70周岁": timee = 70 - datetime.datetime.now().year + Year
                elif Insper == "至60周岁": timee = 60 - datetime.datetime.now().year + Year
                elif Insper == "至66周岁": timee = 66 - datetime.datetime.now().year + Year
                elif Insper == "至77周岁": timee = 77 - datetime.datetime.now().year + Year
                elif Insper == "至80周岁": timee = 80 - datetime.datetime.now().year + Year
                else: timee = 88 - datetime.datetime.now().year + Year
                if int(Payper) > timee: continue
                items = information(Year, Sex, Insper, Payper, Insamo)
                if items:
                    RESULTS.append(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper)+"年交" + "," +str(Insamo)+"万元" + "," + str(items[0]))
                    print(str(datetime.datetime.now().year - int(Year)) + "," + Sex + "," + Insper + "," +
                          str(Payper) + "年交" + "," + str(Insamo) + "万元" + "," + str(items[0]))
    return RESULTS