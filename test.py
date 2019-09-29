import requests
import re

url='https://m.fengjr.com/api/v2/common/backendGetRequireLogin?type=mback&path=%2Faccurate%2Fapi%2Fv1%2Fuser%2Fquestion%3Fmode%3Ddiagnose&_t=1544324415276'
datas = {'type': 'mback',
        'path': '/accurate/api/v1/user/question?mode=diagnose',
        '_t': '1544324415276'}
header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': "keep-alive",
            'Cookie': 'fms-sid=s%3AbvYZ55xHB4KJzoHyEAIICOzNv2RdFuBz.vD50w1LNJ44wXGWpCEB4Usm1c8yc3j6d%2Fc8u4Tjk7p8; gbl_did=1e9c328a-631f-4021-bf14-ab6196878220; abVersion=B; _ga=GA1.2.4037151.1544206676; fjr_channel_code=200034; fjr_did=9f70b309-0edf-4c0c-8e39-6e3bcb8a7460; fjr_fst=1544206676295; fjr_lst=1544206676295; aclc=200034; _gid=GA1.2.1988424153.1544324332; fjr_channel_date=1544324332278; fjr_vts=2; _fjrvts=1; fjr_vct=1544324332278; fjr_internal_ip=192.168.0.10; aclt=1544324332278; __storejs_expire_mixin_closeDownLoad=%221544410735795%22; closeDownLoad=true; __storejs_expire_mixin_centerBankPopup=%221544410780914%22; centerBankPopup=%22hiden%22; fjr_properties=%7B%22browserEnv%22%3A%22app%22%2C%22isLogin%22%3Atrue%7D; fjr_user_id=760D2EAF-128A-46AB-884F-E854015CDBA7; fjr_sqn=9; _gat=1',
            'Host': 'm.fengjr.com',
            'Referer': 'https://m.fengjr.com/cn/re/special/2018/09/intellV4/answerQuestions/diagnose',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
response = requests.get(url,data=datas,headers= header)
content = response.text

pattern = re.compile('"question":"(.*?)".*?"options":(.*?)},"selected"', re.S)
items = re.findall(pattern, str(content))
for it in items:
    print(it[0])
    print(it[1])