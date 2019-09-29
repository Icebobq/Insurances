import pdfplumber
import numpy as np
import pandas as pd
import re

def join_col(index,data):
    dd = data.loc[0:index-1].apply(','.join)
    train_data = np.array(dd)
    train_x_list = train_data.tolist()
    return train_x_list

def standard(content):
    if str(content).find('男') != -1:
        RESULT = "M"
    elif str(content).find('女') != -1:
        RESULT = "F"
    elif str(content).find('终身') != -1:
        RESULT = 'A106'
    elif str(content).find('至') != -1:
        RESULT = 'A' + re.findall("\d+", str(content))[0]
    elif str(content).find('一次') != -1 or str(content).find('趸交') != -1:
        RESULT = 'Y1'
    elif str(content).find('计划') == -1:
        RESULT = 'Y' + re.findall("\d+", str(content))[0]
    else:
        RESULT = content

    return RESULT

def merge(index,datas):
    try:
        int(datas[-1][0][0])
        datas[-2] = datas[-2].append(datas[-1],ignore_index=True)
        datas.pop()
        return datas
    except:
        ddtt = pd.DataFrame([join_col(index,datas[-1])])
        datas[-1] = ddtt.append(datas[-1], ignore_index=True)
        datas[-1] = datas[-1].drop(datas[-1].index[1:index+1])
        return datas

def add_item(data, table):
    if len(data) == 1:
        new_item = [str(data[0])[0:2]+'1'] * (len(table) - len(data))
    else:
        new_item = [data[-1]] * (len(table)-len(data))
    return data+new_item

def add_header(level, Stand, Term, code, table, sex):
    index = 0
    try:
        int(table[0][0])
    except:
        if len(Term) > 1:
            Term = [add_item(Term,table[0])]
            table = Term+table
            index += 1

        if len(sex) > 1:
            sex = [add_item(sex,table[0])]
            table = sex+table
            index += 1

        Stand = [add_item(Stand,table[0])]
        table = Stand+table
        index += 1

        if str(table).find('计划代码') == -1:
            code = [add_item(code, table[0])]
            table = code + table
            index += 1

        level = [add_item(level,table[0])]
        table = level+table
        index += 1

    return table,index

def check_again(table):
    Name = ''
    if table['性别'][1] != 'M' and table['性别'][1] != 'F':
        for index in table.columns.values.tolist():
            if table[index][1] == 'M' or table[index][1] == 'F':
                Name = index
                break
        table.rename(columns={'性别': Name, Name: '性别'}, inplace=True)
    return table

def code_ku(content):
    global code_number,code_dict
    if [content] not in code_dict.values():
        code_number += 1
        code_index = '计划' + str(code_number)
        code_dict[code_index] = [content]
        return code_index
    else:
        for key,value in code_dict.items():
            if value[0] == content:
                return key

product_code = '附加光大永明嘉多保防癌险'
path = product_code+'.pdf'
datas = []
code_number = 0
code_dict = dict()
level = ['风险等级']
code = ['计划代码']
Stand_fee = ['基本保险金额']
Insu_term = ['保险期间']
Sex = ['性别']
with pdfplumber.open(path) as pdf:

    pages = pdf.pages
    for page in pages:
        content = page.extract_text()
        tables = page.extract_tables()
        table_header = content.split('\n')

        for item in table_header:
            paper = tables[0][0][0].split('\n')[0].strip()
            if item.find(paper) != -1:
                break
            if item.find('男') != -1:
                Sex = ['性别']
                Sex.append('M')
            elif item.find('女') != -1:
                Sex = ['性别']
                Sex.append('F')
            if item.find('定期寿险') != -1:
                continue
            if item.find('等级：') != -1:
                level = ['风险等级']
                level.append(item.split('等级：')[1].strip())
            elif item.find('标准') != -1 or item.find('优选') !=-1 or item.find('健康') != -1\
                    or item.find('超优') !=-1:
                level = ['风险等级']
                level.append(item.split('，')[0].split(' ')[0].split('费率')[0].strip('（'))
            if item.find('基本保险金额：') != -1:
                Stand_fee = ['基本保险金额']
                content = item.split('基本保险金额：')[1].split('元')[0]
                content = content.replace(',','')
                Stand_fee.append(content)
            elif item.find('基本保险金额') != -1 or item.find('基本保额') != -1:
                Stand_fee = ['基本保险金额']
                content = item.split('每')[1].split('元')[0].strip()
                content = content.replace(',','')
                Stand_fee.append(content)
            if item.find('保险期间：') != -1:
                content = item.split('保险期间：')[1].split(' ')[0].split('，')[0]
                Insu_term = ['保险期间']
                Insu_term.append(standard(content))
            elif item.find('保险期间') != -1:
                content = item.split('保险期间')[1].split(' ')[0]
                Insu_term = ['保险期间']
                Insu_term.append(standard(content))
            if item.find('基础部分') != -1:
                content = item.split(' ')[0]
                code = ['计划代码']
                code_index = code_ku(content)
                code.append(code_index)

        for table in tables:
            index_row = 0

            for row in table:
                try:
                    int(row[0])
                    break
                except:
                    boollen = row[1]
                    if boollen == None:
                        boollen = row[0]
                        row[1] = boollen
                    if boollen.find('男') != -1 or boollen.find('女') != -1:
                        row[0] = '性别'
                    elif boollen.find('交') != -1:
                        row[0] = '交费方式'
                    elif boollen.find('保') != -1:
                        row[0] = '保险期间'
                    elif boollen.find('基') != -1 or boollen.find('+') != -1:
                        row[0] = '计划代码'
                        code_index = code_ku(boollen)
                        row[1] = code_index

                    # row[0] = row[0].split('\n')[0]
                    # if row[0].find('缴费') != -1 or row[0].find('交费') != -1:
                    #     row[0] = '交费方式'
                    # elif row[0].find('保障') != -1:
                    #     row[0] = '保险期间'
                    # if row[0].find('年龄') != -1:
                    #     continue
                    for index in range(1,len(row)):
                        if row[index] == None:
                            row[index] = row[index-1]
                        else:
                            row[index] = standard(row[index])

                    table[index_row] = row
                    index_row += 1

            table,index_add = add_header(level, Stand_fee, Insu_term, code, table, Sex)
            index_row += index_add
            datas.append(pd.DataFrame(table))
            datas = merge(index_row,datas)

index_data = 0
for data in datas:
    data.columns = join_col(1,data)
    data.drop(index=[0],inplace=True)
    data.set_index(str(data.columns[0]),drop=True,inplace=True)
    data = data.stack()
    data = data.reset_index()
    data.columns = ['年龄',str(data.columns[0]),'费率']
    data = data.mask(data.eq('')).dropna()
    names=data[str(data.columns[1])].str.split(',',expand=True)
    names.columns = str(data.columns[1]).split(',')
    dirc = 1
    for name in names.columns:
        data.insert(dirc, name, names[name])
        dirc += 1
    data.drop(columns=data.columns[dirc],inplace=True)
    data.set_index(str(data.columns[0]),drop=True,inplace=True)
    data = data.reset_index()
    data = check_again(data)
    datas[index_data] = data
    index_data += 1

PRINT = datas[0]
for data in datas[1:]:
    PRINT = PRINT.append(data,ignore_index=True)
PRINT = PRINT[['年龄','风险等级','计划代码','基本保险金额','保险期间','交费方式','性别','费率']]

if code_dict:
    code_df = pd.DataFrame(code_dict).T
    code_df = code_df.reset_index()
    code_df.columns = ['计划代码', '计划内容']
    PRINT[''] = ''
    PRINT = pd.concat([PRINT, code_df], axis=1)

path = product_code+'.xls'
PRINT.to_excel(path,sheet_name='一维费率表')