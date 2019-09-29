import re,requests,csv,time,datetime,sys,queue,asyncio,aiohttp
from requests.packages import urllib3
urllib3.disable_warnings()

class QiXin:
    def __init__(self):
        self.login_url = 'https://www.qixin18.com/loginPost'
        self.login_data = {'mobile': '15800334221',
                            'password': 'xyc123456'}
        self.login_header = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                # 'cookie': 'user_id_set_remember=18138778108; orderTips=true; auth-tips=1; nodejs_sid=s%3APDpXLP3hgNdozXiscKJ5PM0wJXWztJGC.Le89lJSuuA%2B4skJ6josTmdsMo6Vj5aY%2FlatUj6e1R%2BA; hz_guest_key=4rSFbU768HZ25MkM5FKo_1548966788187_0_0; hz_visit_key=3oznTvn8HHZ49A10qOwm_1548966779848_5_1548966779848; hz_view_key=4rSFbU768HZ25MkM5FKo1Nbre28IJHZ42gquOrnZ_1548966845832_https%253A%252F%252Fwww.qixin18.com%252Flogin',
                                'origin': 'https://www.qixin18.com',
                                'referer': 'https://www.qixin18.com/login',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                                'x-requested-with': 'XMLHttpRequest'}
        self.mobile = ''
        self.password = ''
        self.cookie = {}
        self.search_url = 'https://www.qixin18.com/order/searchInsureList'
        self.search_data = {'data[isSubPartner]': '1',
                        'data[partnerId]': 'true',
                        'data[pageModel][pageIndex]': '1',
                        'data[pageModel][pageSize]': '10',
                        'data[timeType]': '0',
                        'data[startTime]': '2019-1-1 00:00:00',
                        'data[endTime]': '2019-1-31 23:59:59',
                        'data[categoryId]': '0',
                        'data[insurantType]': '0',
                        'data[insureType]': '0',
                        'data[state]': '0',
                        'data[orderSource]': '0'}
        self.search_header = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                             # 'cookie': 'user_id_set_remember=18138778108; orderTips=true; nodejs_sid=s%3APDpXLP3hgNdozXiscKJ5PM0wJXWztJGC.Le89lJSuuA%2B4skJ6josTmdsMo6Vj5aY%2FlatUj6e1R%2BA; hz_guest_key=4rSFbU768HZ25MkM5FKo_1548966788187_0_0; needCaptcha=false; auth-tips=1; hz_visit_key=3oznTvn8HHZ49A10qOwm_1548966779848_11_1548966779848; hz_view_key=4rSFbU768HZ25MkM5FKo2iq39omKZHZ25XcT0mE0_1548967399554_https%253A%252F%252Fwww.qixin18.com%252Forder',
                             'origin': 'https://www.qixin18.com',
                             'referer': 'https://www.qixin18.com/order',
                             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                             'x-requested-with': 'XMLHttpRequest'}
        self.startTime = ''
        self.endTime = ''
        self.state = ''
        self.order_url = ''
        self.order_data = {'encryptInsureNum': ''}
        self.order_header = {
                            # 'cookie': 'nodejs_sid=s%3Ajj2LvzSFxeKTt1-i5PIbfAga_NoYEArE.SILkHXF%2FDgqifMJUFHFDEhbcvklO%2FK%2BPKPJ6%2Be7EVPQ; hz_guest_key=34GZPKajNHZ3sb0L1nfv_1549033772680_1_0; hz_visit_key=2qWdz9ySHHZ16V5aKNUy_1549033772680_8_1549033772680; hz_view_key=34GZPKajNHZ3sb0L1nfv3oznY4x8ZHZ20FDgbqFg_1549034265110_https%253A%252F%252Fcps.qixin18.com%252Flzh1042243%252Forder%252Fdetail%253FencryptInsureNum%253Dw*LU5kg8*223j7dwIz30GA%21%21',
                             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.EXIT = False
        self.index = 0
        self.writer = ''
        self.way_name = ['渠道名称', '账户名称', '首年推广费']
        self.order_name = ['序', '保单号', '投保日期', '保单分类', '保单状态']
        self.insuer_name = ['姓名', '身份证', '性别', '出生年月', '投保年龄']
        self.owner_name = ['姓名', '身份证', '是被保人', '微信号', '微信昵称', '手机号码', '邮箱']
        self.produce_name = ['产品名称', '基本保额', '保险期间', '交费期间', '保险起期', '保险止期', '年保费', '支付方式', '银行', '卡号后四位']

    def calculate_age(self, InsuTime, Birth):
        Insu_time = datetime.datetime.strptime(InsuTime, '%Y-%m-%d')
        Birth_time = datetime.datetime.strptime(Birth, '%Y-%m-%d')
        return Insu_time.year - Birth_time.year - ((Insu_time.month, Insu_time.day) < (Birth_time.month, Birth_time.day))

    def view_bar(self, page, num):
        r = u'\r[正在抓取第%d页，第%d个保单，抓取总数目：%d]' % (int(page) , int(num), int(self.index) ,)
        sys.stdout.write(r)
        sys.stdout.flush()

    async def contractWeb(self,url,dat,header,cookie):
        try:
            async with aiohttp.ClientSession(cookies=cookie) as session:
                response = await session.post(url, data=dat, headers=header)
                content = await response.text()
                return content
            # session = aiohttp.ClientSession(cookies=cookie)
            # response = await session.post(url,data=dat,headers=header)
            # content = await response.text()
            # session.close()
            # return content
        except:
            return None

    def owner_detail(self,content,owner_value,insuer_value):
        # ['姓名', '身份证', '是被保人', '微信号', '微信昵称', '手机号码', '邮箱']
        patt = re.compile('<ul class="ul-list.*?>(.*?)</ul>', re.S)
        item = re.findall(patt, content)
        for tt in item:
            pat = re.compile('<li>.*?<span class="name".*?>(.*?)</span>.*?<span>(.*?)</span>.*?</li>', re.S)
            ite = re.findall(pat, tt)
            for kk in ite:
                if str(kk[0].strip()).find('姓名') != -1:
                    owner_value[0] = str(kk[1].strip())
                    insuer_value[0] = owner_value[0]
                elif str(kk[0].strip()).find('证件号码') != -1:
                    owner_value[1] = str(kk[1].strip())+"\t"
                    insuer_value[1] = owner_value[1]
                elif str(kk[0].strip()).find('手机号码') != -1:
                    owner_value[5] = str(kk[1].strip())+"\t"
                elif str(kk[0].strip()).find('邮箱') != -1:
                    owner_value[6] = str(kk[1].strip())
                elif str(kk[0].strip()).find('性别') != -1:
                    insuer_value[2] = str(kk[1].strip())
                elif str(kk[0].strip()).find('出生日期') != -1:
                    insuer_value[3] = str(kk[1].strip())

    def insuer_detail(self,content,owner_value,insuer_value):
        # ['姓名', '身份证', '性别', '出生年月', '投保年龄']
        patt = re.compile('<ul class="ul-list.*?>(.*?)</ul>', re.S)
        item = re.findall(patt, content)
        for tt in item:
            pat = re.compile('<li>.*?<span class="name".*?>(.*?)</span>.*?<span>(.*?)</span>.*?</li>', re.S)
            ite = re.findall(pat, tt)
            for kk in ite:
                if str(kk[0].strip()).find('姓名') != -1:
                    insuer_value[0] = str(kk[1].strip())
                elif str(kk[0].strip()).find('是被保险人的') != -1:
                    owner_value[2] = str(kk[1].strip())
                elif str(kk[0].strip()).find('证件号码') != -1:
                    insuer_value[1] = str(kk[1].strip())+"\t"
                elif str(kk[0].strip()).find('性别') != -1:
                    insuer_value[2] = str(kk[1].strip())
                elif str(kk[0].strip()).find('出生日期') != -1:
                    insuer_value[3] = str(kk[1].strip())

    def pay_detail(self,content,produce_value):
        # ['产品名称','基本保额','保险期间','交费期间','保险起期','保险止期','年保费','支付方式','银行','卡号后四位']
        patt = re.compile('<ul class="ul-list.*?>(.*?)</ul>', re.S)
        item = re.findall(patt, content)
        for tt in item:
            pat = re.compile('<li>.*?<span class="name".*?>(.*?)</span>.*?<span>(.*?)</span>.*?</li>', re.S)
            ite = re.findall(pat, tt)
            for kk in ite:
                if str(kk[0].strip()).find('开户银行') != -1:
                    produce_value[7] = '银行卡'
                    produce_value[8] = str(kk[1].strip())
                elif str(kk[0].strip()).find('银行账号') != -1:
                    produce_value[9] = str(kk[1].strip())[-4:]+"\t"

    def produce_detail(self, content,produce_value,insuer_value):
        # ['产品名称','基本保额','保险期间','交费期间','保险起期','保险止期','年保费','支付方式','银行','卡号后四位']
        patt = re.compile('<table class="policy-item-table".*?>(.*?)</table>', re.S)
        item = re.findall(patt, content)
        for tt in item:
            pat = re.compile('<tr>.*?<td class="td".*?>(.*?)</td>.*?<td class="td".*?>(.*?)</td>.*?</tr>', re.S)
            ite = re.findall(pat, tt)
            for kk in ite:
                if str(kk[0].strip()).find('基本保额') != -1:
                    produce_value[1] = str(kk[1].strip())
                elif str(kk[0].strip()).find('保障期限') != -1:
                    produce_value[2] = str(kk[1].strip())
                    if produce_value[2] == '1年': produce_value[3] = '1年'
                elif str(kk[0].strip()).find('缴费年限') != -1 and str(kk[0].strip()).find('附加') == -1:
                    produce_value[3] = str(kk[1].strip())
                elif str(kk[0].strip()).find('出生日期') != -1:
                    insuer_value[4] = str(kk[1].strip())

    def all_detail(self,orderDetail,owner_value,insuer_value,produce_value,way_value):
        pattern = re.compile(
            '<div class="detail-item bgfw p20 m-t-10">.*?<div class="heading.*?>(.*?)</div>(.*?)</div>', re.S)
        items = re.findall(pattern, orderDetail)
        for it in items:
            if str(it[0].strip()).find('投保人信息') != -1:
                self.owner_detail(it[1],owner_value,insuer_value)
            elif str(it[0].strip()).find('被保险人信息') != -1:
                self.insuer_detail(it[1],owner_value,insuer_value)
            elif str(it[0].strip()).find('缴费信息') != -1:
                self.pay_detail(it[1],produce_value)
            elif str(it[0].strip()).find('投保信息') != -1:
                self.produce_detail(it[1],produce_value,insuer_value)

    async def record(self,index,pageIndex,order):
        # ['产品名称','基本保额','保险期间','交费期间','保险起期','保险止期','年保费','支付方式','银行','卡号后四位']
        owner_value = [''] * len(self.owner_name)
        insuer_value = [''] * len(self.insuer_name)
        produce_value = [''] * len(self.produce_name)
        way_value = [''] * len(self.way_name)
        order_value = [str(index), str(order["insureNum"]) + "\t", str(order["createTime"]).split(' ')[0], '',
                       str(order["stateDesc"])]
        produce_value[0] = str(order['productName'])
        produce_value[4] = str(order['startDate']).split(' ')[0]
        produce_value[5] = str(order['endDate']).split(' ')[0]
        produce_value[6] = str(abs(float(order['price'])/100)) + "\t"
        way_value[0] = '齐欣云服'
        self.order_url = 'https://cps.qixin18.com/' + order['domain'] + '/order/detail?encryptInsureNum=' + order[
            'encryptInsureNum']
        self.order_data['encryptInsureNum'] = order['encryptInsureNum']
        order_detail = await self.contractWeb(self.order_url, self.order_data, self.order_header, self.cookie)
        if not order_detail:
            await self.record(index,pageIndex,order)
            #print(u'\n---第'+str(pageIndex)+'页，订单'+str(order["insureNum"])+'，抓取失败---')
        else:
            self.all_detail(order_detail,owner_value,insuer_value,produce_value,way_value)
            if insuer_value[4] == '':
                insuer_value[4] = str(self.calculate_age(order_value[2],insuer_value[3]))+'周岁'
            if order_value[4] == '':
                order_value[4] = '扣款中'
            All = order_value + owner_value + insuer_value + produce_value + way_value
            self.writer.writerow(All) 
            self.view_bar(pageIndex, index)

    async def process(self,pageIndex):
        self.search_data['data[pageModel][pageIndex]'] = str(pageIndex)
        content = await self.contractWeb(self.search_url, self.search_data, self.search_header,self.cookie)
        true = True
        false = False
        # print(content)
        content = eval(content)
        if content['data']['data'] == []:
            self.EXIT = True
        else:
            for order in content['data']['data']:
                self.index += 1
                await self.record(self.index,pageIndex,order)
            # new_tasks = [asyncio.ensure_future(self.record(pageIndex,order)) for order in content['data']['data']]
            # new_loop = asyncio.get_event_loop()
            # new_loop.run_until_complete(asyncio.gather(new_tasks))

    def start(self):
        print(u'----------登录阶段----------')
        # self.mobile = input(u'手机号：')
        # self.password = input(u'密码：')
        # self.login_data['mobile'] = self.mobile
        # self.login_data['password'] = self.password
        # try:
        response = requests.post(self.login_url, data=self.login_data, headers=self.login_header,verify=False)
        cookie = response.cookies
        self.cookie = requests.utils.dict_from_cookiejar(cookie)
        print(u'----------登录成功----------\n')
        # except:
        #     print(u"----------登录失败----------\n")
        #     return None

        print(u'----------筛选阶段----------')
        while(1):
            case = input(u"时间范围筛选： 1、指定起始和截止时间  2、只指定起始时间  3、只指定截止时间  4、所有保单，不指定时间\n"
                         u"（ 提醒：起始时间和截止时间都为日期 / 输入格式例如：2019-1-31 ）\n")
            if case == '1':
                self.startTime = input(u"起始时间：")
                self.endTime = input(u"截止时间：")
                break
            elif case == '2':
                self.startTime = input(u"起始时间：")
                self.endTime = datetime.date.today().strftime('%Y-%m-%d')
                break
            elif case == '3':
                self.startTime = '1000-1-1'
                self.endTime = input(u"截止时间：")
                break
            elif case == '4':
                self.startTime = '1000-1-1'
                self.endTime = datetime.date.today().strftime('%Y-%m-%d')
                break
            else:
                print(u'---输入错误，请重新选择---')
        self.search_data['data[startTime]'] = self.startTime + ' 00:00:00'
        self.search_data['data[endTime]'] = self.endTime + ' 23:59:59'
        while(1):
            case = input(u"订单状态筛选： 1、未支付  2、已支付  3、退保单  4、所有保单\n")
            if case != '1' and case != '2' and case != '3' and case != '4':
                print(u'---输入错误，请重新选择---')
            else:
                if case == '3':
                    self.search_data['data[state]'] = '4'
                elif case == '4':
                    self.search_data['data[state]'] = '0'
                else:
                    self.search_data['data[state]'] = case
                break
        print(u'----------筛选成功----------\n')

        print(u'----------抓取阶段----------')

        start_time = time.time()

        f = open("Orders_detail.csv", 'w', newline='')
        self.writer = csv.writer(f)
        All = ['']*(len(self.order_name)+len(self.owner_name)+len(self.insuer_name)+len(self.produce_name)+len(self.way_name))
        All[0] = '保单基本信息'
        All[len(self.order_name)] = '投保人信息'
        All[len(self.order_name)+len(self.owner_name)] = '被保人信息'
        All[len(self.order_name) + len(self.owner_name)+len(self.insuer_name)] = '产品信息'
        All[len(self.order_name) + len(self.owner_name) + len(self.insuer_name)+len(self.produce_name)] = '渠道信息'
        self.writer.writerow(All)
        All = self.order_name + self.owner_name + self.insuer_name + self.produce_name + self.way_name
        self.writer.writerow(All)
        pageIndex = 0
        while(1):
            if self.EXIT:
                break
            pageIndex += 1
            tasks = [asyncio.ensure_future(self.process(page)) for page in range((pageIndex-1)*60+1,pageIndex*60+1)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))

        f.close()
        end_time = time.time()
        print(u'\n总耗时：'+str(end_time-start_time)+'s')
        print(u'----------抓取结束----------')

First_open = QiXin()
First_open.start()


