#-*- coding:utf-8 -*-
from pulp import *
import re
import sys
import os

Insurance_name = []
Insurance_code = []
Insurance_amount = {}
Insurance_fee = {}

# 文件输入控制
f1 = open("Options_Result.txt", "w", encoding='utf-8')  # 打开文件

def resource_path(path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    #print(os.path.join(base_path, path))
    return os.path.join(base_path, path)

filename = 'Options.txt'
with open(resource_path(filename), 'r', encoding='utf-8') as f2:
    for i in f2:
        split = i.split(",")
        Insurance_name.append(str(split[0]))
        Code = str(split[0]).split("——")
        if len(Insurance_code) > 0 and int(Insurance_code[len(Insurance_code)-1]['code']) == str(Code[0]):
            Insurance_code[len(Insurance_code) - 1]['children'].append(str(split[0]))
        else:
            Insurance_code.append({'code':str(Code[0]),'children':[str(split[0])]})
        mode = re.compile(r'\d+')
        amount = mode.findall(str(split[1]))
        Insurance_amount[str(split[0])] = int(amount[0])
        fee = mode.findall(str(split[2]))
        Insurance_fee[str(split[0])] = float(fee[0])

Amount = input("请输入指定的总保额（万元）：")
#创建问题实例，求最小极值
prob = LpProblem("The Optimal Insurance Product portfolio Problem", LpMinimize)

#构建Lp变量字典
ingredient_vars = LpVariable.dicts("Insurance",Insurance_name,lowBound=0,upBound=1,cat=LpInteger)

#添加目标方程
prob += lpSum([Insurance_fee[i]*ingredient_vars[i] for i in Insurance_name])

#添加约束条件
prob += lpSum([Insurance_amount[i] * ingredient_vars[i] for i in Insurance_name]) >= int(Amount)
for it in Insurance_code:
    prob += lpSum([ingredient_vars[i] for i in it['children']]) <= 1

#求解
prob.solve()
#查看解的状态
print("Status:", LpStatus[prob.status])
f1.write("Status:"+str(LpStatus[prob.status])+"\n")
#查看解
Total_amount = 0
Total_fee = 0
print("方案：")
f1.write("方案："+"\n")
for i in Insurance_name:
    if ingredient_vars[i].value() != 0:
        Total_fee = Total_fee + Insurance_fee[i]
        Total_amount = Total_amount + Insurance_amount[i]
        print(str(ingredient_vars[i])+","+str(Insurance_amount[i])+"万元,"+str(Insurance_fee[i]))
        f1.write(str(ingredient_vars[i]) + "," + str(Insurance_amount[i]) + "万元," + str(Insurance_fee[i])+"\n")
    #print(ingredient_vars[i],"=",ingredient_vars[i].value())
print("总保额：" + str(Total_amount) + "万元")
f1.write("总保额：" + str(Total_amount) + "万元"+"\n")
print("总费用："+str(Total_fee)+"元")
f1.write("总费用："+str(Total_fee)+"元"+"\n")
f1.close()
input("系统：结果已显示，按任意键退出程序！")