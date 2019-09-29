import pandas as pd
import re,os,sys

def get_file(path,left,right):
    f = os.listdir(path)
    left_name = left + '.xls'
    right_name = right + '.xls'
    if left_name not in f:
        print('找不到文件：'+left_name)
        return None
    elif right_name not in f:
        print('找不到文件：'+right_name)
        return None

    excelFile_left = os.path.join(path, left_name)
    excelFile_right = os.path.join(path, right_name)

    return excelFile_left,excelFile_right

def get_comb_and_path():
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    aim_path = os.path.join(base_path,'待组合区')
    f = os.listdir(aim_path)
    print('******************')
    print('检查到以下产品：')
    number = 0
    product = []
    for file in f:
        file_name = str(file.split('.')[0])
        if file_name.find('+') != -1: continue
        if file_name.find('主险') !=-1:
            number += 1
            product.append(file_name)
            print(str(number) + '、' + file_name, end='\t')
            break
    for file in f:
        file_name = str(file.split('.')[0])
        if file_name.find('+') != -1: continue
        if file_name.find('主险') != -1:
            continue
        number += 1
        product.append(file_name)
        print(str(number)+'、'+file_name,end='\t')
    print('\n******************')
    print('请输入组合：  (输入方式：1、输入\'None\'代表结束；2、按照上述编号和主+附的顺序输入组合，例如\'1+2+3\'；3、回车输入新组合)')
    number = 0
    comb = []
    bool = True
    while(1):
        if bool:
            number+=1
        bool = True
        inp = input('第'+str(number)+'个组合：')
        if inp == 'None':
            break
        else:
            check = inp.split('+')
            check = list(map(int, check))
            if max(check) > len(product):
                bool = False
                print('******************')
                print('输入错误，无该产品，请重新输入！')
                print('******************')
                continue
        comb.append(check)
        # comb.append([product[i-1] for i in check])

    comb.sort(reverse=False)
    return comb,aim_path,product

comb_list,path,product = get_comb_and_path()
excelFile_main = os.path.join(path, product[0]+'.xls')
df_one = pd.DataFrame(pd.read_excel(excelFile_main))
del df_one['Unnamed: 0']
code_number = 1
code_dict = {'计划1': [product[0]]}

number = 0
for comb in comb_list:
    number += 1
    print('******************')
    print('正在生成第'+str(number)+'个组合...')
    comb = [product[i-1] for i in comb]
    new_comb = "+".join(comb)
    code_number += 1
    code_name = '计划'+str(code_number)
    code_dict[code_name] = [new_comb]
    right = comb[-1]
    comb.pop()
    left = "+".join(comb)
    excelFile_left, excelFile_right = get_file(path,left,right)

    df_origin_left = pd.DataFrame(pd.read_excel(excelFile_left))
    del df_origin_left['Unnamed: 0']

    df_origin_right = pd.DataFrame(pd.read_excel(excelFile_right))
    del df_origin_right['Unnamed: 0']

    table_name = df_origin_left.columns.values.tolist()
    table_name = dict(zip(table_name,['']*len(table_name)))
    df_new = pd.DataFrame(columns=table_name)

    for index in range(len(df_origin_right)):

        row = df_origin_right.loc[index]
        df_fitted = df_origin_left.loc[df_origin_left['年龄'] == row['年龄']].loc[df_origin_left['风险等级'] == row['风险等级']].\
            loc[df_origin_left['基本保险金额'] == row['基本保险金额']].loc[df_origin_left['保险期间'] == row['保险期间']].\
            loc[df_origin_left['交费方式'] == row['交费方式']].loc[df_origin_left['性别'] == row['性别']]

        if len(df_fitted) > 1:
            print('出现多项匹配，请核查！')
            continue

        df_fitted['费率'] += row['费率']
        d_index = list(df_fitted.columns).index('计划代码')
        # if df_fitted.iloc[0,d_index] == '默认':
        #     df_fitted.iloc[0,d_index] = '计划1'
        # else:
        #     df_fitted.iloc[0,d_index] = '计划' + str(int(re.findall("\d+", str(df_fitted['计划代码']))[0])+1)
        df_fitted.iloc[0, d_index] = code_name

        df_new = pd.concat([df_new, df_fitted], axis=0)
        df_new = df_new.reset_index()
        del df_new['index']

    path = os.path.join(path,new_comb+'.xls')
    df_new.to_excel(path,sheet_name='一维费率表')

    df_one = pd.concat([df_one, df_new], axis=0)
    df_one = df_one.reset_index()
    del df_one['index']

if code_dict:
    code_df = pd.DataFrame(code_dict).T
    code_df = code_df.reset_index()
    code_df.columns = ['计划代码', '计划内容']
    df_one[''] = ''
    df_one = pd.concat([df_one, code_df], axis=1)

path = product[0].split('_')[0]+'.xls'
df_one.to_excel(path, sheet_name='一维费率表')