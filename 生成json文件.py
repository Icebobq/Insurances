import re
import json
import requests

Jobs = []
url = 'http://weixin.hongkang-life.com/hk/dqLife2019/occupation'
response = requests.post(url,verify=False)
content = response.text

pattern = re.compile('"coreCode":"(.*?)".*?"name":"(.*?)".*?"category":(.*?),',re.S)
items = re.findall(pattern, str(content))
for it in items:
    if it[2] == 'null':
        Jobs.append({"coreCode":str(it[0]),"name":str(it[1]),"category":it[2],"children":[]})
    else:
        Jobs.append({"coreCode": str(it[0]), "name": str(it[1]), "category": eval(it[2])})

numb = 0
while numb < len(Jobs):
    print("numb="+str(numb))
    data = {"parentId":Jobs[numb]['coreCode']}
    response = requests.post(url, data=data, verify=False)
    content = response.text
    pattern = re.compile('"coreCode":"(.*?)".*?"name":"(.*?)".*?"category":(.*?),',re.S)
    items = re.findall(pattern, str(content))
    for it in items:
        if it[2] == 'null':
            Jobs[numb]['children'].append({"coreCode":str(it[0]),"name":str(it[1]),"category":it[2],"children":[]})
        else:
            Jobs[numb]['children'].append({"coreCode": str(it[0]), "name": str(it[1]), "category": eval(it[2])})
    index = 0
    while index < len(Jobs[numb]['children']):
        print("index="+str(index))
        data = {"parentId":Jobs[numb]['children'][index]['coreCode']}
        response = requests.post(url, data=data, verify=False)
        content = response.text
        pattern = re.compile('"coreCode":"(.*?)".*?"name":"(.*?)".*?"category":(.*?),',re.S)
        items = re.findall(pattern, str(content))
        for it in items:
            if it[2] == 'null':
                Jobs[numb]['children'][index]['children'].append({"coreCode":str(it[0]),"name":str(it[1]),"category":it[2],"children":[]})
                print("************************************************")
            else:
                Jobs[numb]['children'][index]['children'].append({"coreCode": str(it[0]), "name": str(it[1]), "category": eval(it[2])})
        index = index + 1
    numb = numb + 1
file_name = 'Jobs.json'
with open(file_name,'w',encoding='utf-8') as file_object:
    json.dump(Jobs,file_object)