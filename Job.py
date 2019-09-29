#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入json文件
import json
import sys
import os

def resource_path(path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, path)

filename = 'Jobs.json'
with open(resource_path(filename), 'r', encoding='utf-8') as file:
    job_data = json.load(file)

# 打印第一级工作列表的函数
def print_pro():
    count = 0
    for i in range(len(job_data)):
        count += 1
        print(job_data[i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

# 打印第二级工作列表的函数
def print_city(job_num):
    count = 0
    for i in range(len(job_data[job_num]['children'])):
        count += 1
        print(job_data[job_num]['children'][i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

# 打印第三级工作列表的函数
def print_area(job_num, area_num):
    count = 0
    for i in range(len(job_data[job_num]['children'][area_num]['children'])):
        count += 1
        print(job_data[job_num]['children'][area_num]['children'][i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

def start():
    # 定位标志
    loca_num = 0
    # 记录职业代码
    loca_code = ['','','']
    # 记录职业名称
    loca_name = ['', '', '']
    # 记录职业类型
    loca_category = ''

    while True:
        # 打印省级
        if loca_num == 0:
            print_pro()
            loca_num = 1

        if loca_num == 1:
            try:
                into_job_num = input(u'请输入第一级职业编号进入第二级：')
                if int(into_job_num) >= 0 and int(into_job_num) < len(job_data):
                    into_job_num = int(into_job_num)
                    if loca_num == 1:
                        loca_code[loca_num-1] = job_data[into_job_num]['coreCode']
                        loca_name[loca_num - 1] = job_data[into_job_num]['name']
                        print_city(into_job_num)
                    loca_num = 2
                else:
                    print(u'请输入有效数字。')
            except:
                loca_code[0] = job_data[into_job_num]['coreCode']
                loca_code[1] = job_data[into_job_num]['coreCode']
                loca_code[2] = job_data[into_job_num]['coreCode']
                loca_name[0] = job_data[into_job_num]['name']
                loca_name[1] = job_data[into_job_num]['name']
                loca_name[2] = job_data[into_job_num]['name']
                loca_category = job_data[into_job_num]['category']
                return(loca_code,loca_name,loca_category)

        if loca_num == 2:
            try:
                into_area_num = input(u'请输入第二级职业编号进入第三级，输入"r"返回上一级：')
                if into_area_num == 'r':
                    loca_num = 0
                    continue
                elif int(into_area_num) >= 0 and int(into_area_num) < len(job_data[into_job_num]['children']):
                    into_area_num = int(into_area_num)
                    if loca_num == 2:
                        loca_code[loca_num - 1] = job_data[into_job_num]['children'][into_area_num]['coreCode']
                        loca_name[loca_num - 1] = job_data[into_job_num]['children'][into_area_num]['name']
                        print_area(into_job_num, into_area_num)
                    loca_num = 3
                else:
                    print(u'请输入有效数字。')
            except:
                loca_code[1] = job_data[into_job_num]['children'][into_area_num]['coreCode']
                loca_code[2] = job_data[into_job_num]['children'][into_area_num]['coreCode']
                loca_name[1] = job_data[into_job_num]['children'][into_area_num]['name']
                loca_name[2] = job_data[into_job_num]['children'][into_area_num]['name']
                loca_category = job_data[into_job_num]['children'][into_area_num]['category']
                return (loca_code,loca_name,loca_category)

        if loca_num == 3:
            input_in_area = input(u'请输入第三级职业编号，输入"r"返回上一级：')
            if input_in_area == 'r':
                loca_num = 2
                print_city(into_job_num)
                continue
            elif int(input_in_area) >= 0 and int(input_in_area) < len(job_data[into_job_num]['children'][into_area_num]['children']):
                input_in_area = int(input_in_area)
                if loca_num == 3:
                    loca_code[loca_num - 1] = job_data[into_job_num]['children'][into_area_num]['children'][input_in_area]['coreCode']
                    loca_name[loca_num - 1] = job_data[into_job_num]['children'][into_area_num]['children'][input_in_area]['name']
                    print(u"请确认地区信息："+job_data[into_job_num]['name']+"——"+
                          job_data[into_job_num]['children'][into_area_num]['name']+"——"+
                          job_data[into_job_num]['children'][into_area_num]['children'][input_in_area]['name'])
                    input_final = input(u'输入"q"确认职业信息，输入"r"返回上一级：')
                    if input_final == 'r':
                        loca_num = 3
                        print_area(into_job_num, into_area_num)
                        continue
                    elif input_final == 'q':
                        loca_category = job_data[into_job_num]['children'][into_area_num]['children'][input_in_area]['category']
                        return(loca_code,loca_name,loca_category)
                    else:
                        print(u"请输入有效符号。")
            else:
                print(u"请输入有效数字。")
