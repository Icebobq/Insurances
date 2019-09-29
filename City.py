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

filename = 'City_json_new.json'
with open(resource_path(filename), 'r') as file:
    china_data = json.load(file)

# 打印省级的函数
def print_pro():
    count = 0
    for i in range(len(china_data)):
        count += 1
        print(china_data[i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

# 打印市级的函数
def print_city(city_num):
    count = 0
    for i in range(len(china_data[city_num]['children'])):
        count += 1
        print(china_data[city_num]['children'][i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

# 打印县级的函数
def print_area(city_num, area_num):
    count = 0
    for i in range(len(china_data[city_num]['children'][area_num]['children'])):
        count += 1
        print(china_data[city_num]['children'][area_num]['children'][i]['name'].ljust(8,'>'),'%02d'.ljust(6,' ') % i, end='')
        # 用于打印成3列
        if count % 3 == 0:
            print('')
    if count % 3 != 0:
        print('')

def start():
    # 定位标志
    loca_num = 0
    # 记录地区代码
    loca_code = ['','','']
    # 记录地区名称
    loca_name = ['', '', '']

    while True:
        # 打印省级
        if loca_num == 0:
            print_pro()
            loca_num = 1

        if loca_num == 1:
            try:
                into_city_num = input(u'请输入省级编号进入市级：')
                if int(into_city_num) >= 0 and int(into_city_num) < len(china_data):
                    into_city_num = int(into_city_num)
                    if loca_num == 1:
                        loca_code[loca_num-1] = china_data[into_city_num]['code']
                        loca_name[loca_num - 1] = china_data[into_city_num]['name']
                        print_city(into_city_num)
                    loca_num = 2
                else:
                    print(u'请输入有效数字。')
            except:
                loca_code[0] = china_data[into_city_num]['code']
                loca_code[1] = china_data[into_city_num]['code']
                loca_code[2] = china_data[into_city_num]['code']
                loca_name[0] = china_data[into_city_num]['name']
                loca_name[1] = china_data[into_city_num]['name']
                loca_name[2] = china_data[into_city_num]['name']
                return(loca_code,loca_name)

        if loca_num == 2:
            try:
                into_area_num = input(u'请输入市级编号进入县级，输入"r"返回上一级：')
                if into_area_num == 'r':
                    loca_num = 0
                    continue
                elif int(into_area_num) >= 0 and int(into_area_num) < len(china_data[into_city_num]['children']):
                    into_area_num = int(into_area_num)
                    if loca_num == 2:
                        loca_code[loca_num - 1] = china_data[into_city_num]['children'][into_area_num]['code']
                        loca_name[loca_num - 1] = china_data[into_city_num]['children'][into_area_num]['name']
                        print_area(into_city_num, into_area_num)
                    loca_num = 3
                else:
                    print(u'请输入有效数字。')
            except:
                loca_code[1] = china_data[into_city_num]['children'][into_area_num]['code']
                loca_code[2] = china_data[into_city_num]['children'][into_area_num]['code']
                loca_name[1] = china_data[into_city_num]['children'][into_area_num]['name']
                loca_name[2] = china_data[into_city_num]['children'][into_area_num]['name']
                return (loca_code,loca_name)

        if loca_num == 3:
            input_in_area = input(u'请输入县级编号，输入"r"返回上一级：')
            if input_in_area == 'r':
                loca_num = 2
                print_city(into_city_num)
                continue
            elif int(input_in_area) >= 0 and int(input_in_area) < len(china_data[into_city_num]['children'][into_area_num]['children']):
                input_in_area = int(input_in_area)
                if loca_num == 3:
                    loca_code[loca_num - 1] = china_data[into_city_num]['children'][into_area_num]['children'][input_in_area]['code']
                    loca_name[loca_num - 1] = china_data[into_city_num]['children'][into_area_num]['children'][input_in_area]['name']
                    print(u"请确认地区信息："+china_data[into_city_num]['name']+"——"+
                          china_data[into_city_num]['children'][into_area_num]['name']+"——"+
                          china_data[into_city_num]['children'][into_area_num]['children'][input_in_area]['name'])
                    input_final = input(u'输入"q"确认地区信息，输入"r"返回上一级：')
                    if input_final == 'r':
                        loca_num = 3
                        print_area(into_city_num, into_area_num)
                        continue
                    elif input_final == 'q':
                        return(loca_code,loca_name)
                    else:
                        print(u"请输入有效符号。")
            else:
                print(u"请输入有效数字。")
