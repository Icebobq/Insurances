print("请耐心等待程序启动！")

import ZXBCZAYX
#import ZXBCZAYXZQB
import PARSXA
import BNDHB
import RTRH
import ZHWAB
import GFYSWY
import ZHRSPGBZB
import ZHRSPGYXB
import XMXHQTZYXB
import XMXHQTZBZB
import HGDM
import HKDBZN
import City
import Job
import datetime

class DQSX_System:
    def __init__(self):
        self.age = 0 #年龄
        self.sex = '' #性别
        self.weight = 0 #体重（公斤）
        self.height = 0 #身高（米）
        self.Insper = "无" #保障期间
        self.Payper = -1 #交费期间(年交)
        self.minInsamo = 0 #最低保额(万元)
        self.maxInsamo = 10000000  # 最高保额(万元)
        self.address = [[],[]] #地区
        self.address_SIN = [[],[]] #社保所在地
        self.Job = [[],[],''] # 职业
        self.Smoke = "不提供" #吸烟状况
        self.Healthy = "不提供" #体检状况
        self.SIN = "不提供" #社保状况
        self.product = ['中信保诚祯爱优选定期寿险','平安【人寿】小安定期寿险','百年定惠保定期寿险',
                        '瑞泰瑞和定期寿险','中华为爱保定期寿险','国富一世无忧定期寿险',
                        '中韩【人寿】盘古定期寿险标准版','中韩【人寿】盘古定期寿险优选版','信美相互擎天柱定期寿险2号优选版',
                        '信美相互擎天柱定期寿险2号标准版','华贵大麦定期寿险','弘康大白智能'] #'中信保诚祯爱优选定期寿险增强版'
        self.productfile = [ZXBCZAYX, PARSXA, BNDHB, RTRH, ZHWAB, GFYSWY, ZHRSPGBZB, ZHRSPGYXB,
                            XMXHQTZYXB, XMXHQTZBZB, HGDM, HKDBZN] #ZXBCZAYXZQB

    def calculate_age(self, Birth):
        today = datetime.date.today()
        return today.year - Birth.year - ((today.month, today.day) < (Birth.month, Birth.day))

    def BMI(self,weight,height):
        return float(weight)/float(height)/float(height)

    def start(self):

        Birth = input(u"请输入客户出生日期（例如：2018-1-1）：")  # 整数
        Birth = datetime.datetime.strptime(Birth, "%Y-%m-%d")
        self.age = self.calculate_age(Birth.date())

        self.sex = input(u"请输入客户性别（男/女）：")  # 等待输入
        self.weight = input(u"请输入客户体重（公斤）：")  # 等待输入
        self.height = input(u"请输入客户身高（cm）：")  # 等待输入

#######################################################################功能尚未完善
        BMI = self.BMI(self.weight,float(self.height)/100) # 计算BMI

        print(u"客户吸烟状况：" + "\n" + u"1、不吸烟   2、每天小于10支   3、每天10-20支   4、每天20支以上")
        while True:
            input_Smoke = input(u"请输入对应数字：")
            if input_Smoke == '1':
                self.Smoke = "不吸烟"
                break
            elif input_Smoke == '2':
                self.Smoke = "每天小于10支"
                break
            elif input_Smoke == '3':
                self.Smoke = "每天10-20支"
                break
            elif input_Smoke == '4':
                self.Smoke = "每天20支以上"
                break
            else:
                print(u"请输入有效数字。")

        print(u"客户社保状况：" + "\n" + u"1、有社保   2、无社保")
        while True:
            input_SIN = input(u"请输入对应数字：")
            if input_SIN == '1':
                self.SIN = "有社保"
                break
            elif input_SIN == '2':
                self.SIN = "无社保"
                break
            else:
                print(u"请输入有效数字。")

#######################################################################功能尚未完善
        # input_type = input(u"是否有客户年收入信息？（是/否）（注意：最优保险组合分配此项输入否！）")
        # if input_type == "是":
        Insamo = input(u"请输入客户年收入（万元）：")  # 整数
        self.minInsamo = int(Insamo) * 5
        self.maxInsamo = int(Insamo) * 10
            # print(u"系统：推荐保额范围为"+str(self.minInsamo)+"——"+str(self.maxInsamo)+u"万元！")

        # timee = 0
        input_type = input(u"是否有指定的保障期间要求？（是/否）")
        if input_type == "是":
            print(u"所有提供的保障期间选择：" + "\n" +
                  u"1、保20年   2、保30年   3、至60周岁   4、至65周岁   5、至66周岁"+"\n"+
                  u"6、至70周岁   7、至75周岁   8、至77周岁   9、至80周岁   10、至88周岁")
            while True:
                input_Insper = input(u"请输入指定的保障期间：")
                if input_Insper == '1':
                    self.Insper = "保20年"
                    # timee = 20
                    break
                elif input_Insper == '2':
                    self.Insper = "保30年"
                    # timee = 30
                    break
                elif input_Insper == '3':
                    self.Insper = "至60周岁"
                    # timee = 60 - self.age
                    break
                elif input_Insper == '4':
                    self.Insper = "至65周岁"
                    # timee = 65 - self.age
                    break
                elif input_Insper == '5':
                    self.Insper = "至66周岁"
                    # timee = 66 - self.age
                    break
                elif input_Insper == '6':
                    self.Insper = "至70周岁"
                    # timee = 70 - self.age
                    break
                elif input_Insper == '7':
                    self.Insper = "至75周岁"
                    # timee = 75 - self.age
                    break
                elif input_Insper == '8':
                    self.Insper = "至77周岁"
                    # timee = 77 - self.age
                    break
                elif input_Insper == '9':
                    self.Insper = "至80周岁"
                    # timee = 80 - self.age
                    break
                elif input_Insper == '10':
                    self.Insper = "至88周岁"
                    # timee = 88 - self.age
                    break
                else:
                    print(u"请输入有效数字。")

        input_type = input(u"是否有指定的交费期间要求？（是/否）")
        if input_type == "是":
            print(u"所有提供的交费期间选择：" + "\n" +
                  u"1、1年交   2、3年交   3、5年交   4、10年交   5、20年交   6、30年交   7、至60周岁   8、至70周岁")
            while True:
                input_Payper = input(u"请输入指定的交费期间：")  # 整数
                if input_Payper == '1':
                    self.Payper = "1"
                elif input_Payper == '2':
                    self.Payper = "3"
                elif input_Payper == '3':
                    self.Payper = "5"
                elif input_Payper == '4':
                    self.Payper = "10"
                elif input_Payper == '5':
                    self.Payper = "20"
                elif input_Payper == '6':
                    self.Payper = "30"
                elif input_Payper == '7':
                    self.Payper = "至60周岁"
                elif input_Payper == '8':
                    self.Payper = "至70周岁"
                else:
                    print(u"请输入有效数字。")
                # if int(self.Payper) > timee:
                #     print(u"系统提示：指定交费期间大于指定保障期间，请重新选择！")
                # else:
                #     break

        print(u"请按操作提示依次输入客户所在地区：")
        self.address = City.start()

        if self.SIN == "有社保":
            print(u"客户社保所在地是否与客户所在地区相同？"+"\n"+"1、相同   2、不相同")
            while True:
                input_SIN = input(u"请输入对应数字：")
                if input_SIN == '2':
                    print(u"请按操作提示依次输入客户社保所在地：")
                    self.address_SIN = City.start()
                    break
                if input_SIN == '1':
                    self.address_SIN = self.address
                    break
                else:
                    print(u"请输入有效数字。")

        print(u"请按操作提示依次输入客户职业：")
        self.Job = Job.start()

        f1.write("*******客户保险信息核对*******" + "\n")
        f1.write("出生日期："+str(Birth.date()) + "\n")
        f1.write("对应年龄：" + str(self.age) + "岁" + "\n")
        f1.write("性别：" + str(self.sex) + "\n")
        f1.write("体重：" + str(self.weight) + "公斤" + "\n")
        f1.write("身高：" + str(self.height) + "米" + "\n")
        f1.write("对应BMI值：" + str(BMI) + "\n")
        f1.write("吸烟状况：" + str(self.Smoke) + "\n")
        f1.write("社保状况：" + str(self.SIN) + "\n")
        if self.minInsamo != 0:
            f1.write("年收入：" + str(self.minInsamo/5) + "万元" + "\n")
        else:
            f1.write("年收入：无" + "\n")
        if self.Insper != "无":
            f1.write("指定的保障期间：" + str(self.Insper) + "\n")
        else:
            f1.write("指定的保障期间：无" + "\n")
        if self.Payper != -1:
            f1.write("指定的交费期间：" + str(self.Payper) + "年交" + "\n")
        else:
            f1.write("指定的交费期间：无" + "\n")
        f1.write("所在地区：" + self.address[1][0] + "——" +
                 self.address[1][1] + "——" +
                 self.address[1][2] + "\n")
        if self.SIN == "有社保":
            f1.write("社保所在地：" + self.address_SIN[1][0] + "——" +
                     self.address_SIN[1][1] + "——" +
                     self.address_SIN[1][2] + "\n")
        f1.write("职业：" + self.Job[1][0] + "——" +
                 self.Job[1][1] + "——" +
                 self.Job[1][2] + "\n")
        f1.write("职业类型：第" + self.Job[2] + "类" + "\n")
        f1.write("****************************" + "\n")

        print("*******客户保险信息核对*******")
        print("出生日期："+str(Birth.date()))
        print("对应年龄：" + str(self.age) + "岁")
        print("性别：" + str(self.sex))
        print("体重：" + str(self.weight) + "公斤")
        print("身高：" + str(self.height) + "米")
        print("对应BMI值：" + str(BMI))
        print("吸烟状况：" + str(self.Smoke))
        print("社保状况：" + str(self.SIN))
        if self.minInsamo != 0:
            print("年收入：" + str(self.minInsamo/5) + "万元")
        else:
            print("年收入：无")
        if self.Insper != "无":
            print("指定的保障期间：" + str(self.Insper))
        else:
            print("指定的保障期间：无")
        if self.Payper != -1:
            print("指定的交费期间：" + str(self.Payper) + "年交")
        else:
            print("指定的交费期间：无")
        print("所在地区：" + self.address[1][0] + "——" +
                 self.address[1][1] + "——" +
                 self.address[1][2])
        if self.SIN == "有社保":
            print("社保所在地：" + self.address_SIN[1][0] + "——" +
                     self.address_SIN[1][1] + "——" +
                     self.address_SIN[1][2])
        print("职业：" + self.Job[1][0] + "——" +
                 self.Job[1][1] + "——" +
                 self.Job[1][2])
        print("职业类型：第" + self.Job[2] + "类")
        print("****************************")
        # print(self.address)
        # print(self.Job)
        index = 0
        while index < len(self.product):
            print("")
            f1.write("\n")
            # f1.write("第" + str(index + 1) + "个产品——")
            f1.write(self.product[index]+"："+"\n")
            print(self.product[index]+"：")
            file = self.productfile[index]
            if file == HKDBZN:
                Results = file.start(self.address, datetime.datetime.now().year - int(self.age),
                                  self.sex, int(Insamo), self.minInsamo, self.maxInsamo, self.Insper, self.Payper,
                                  self.Smoke, self.height, self.weight, self.Job)
            else:
                if self.Smoke != '不吸烟': self.Smoke = '吸烟'
                Results = file.start( self.address, datetime.datetime.now().year - int(self.age),
                                  self.sex, self.minInsamo, self.maxInsamo, self.Insper, self.Payper,
                                  self.Smoke, self.Healthy, self.SIN, self.address_SIN, BMI, self.Job)
            if Results:
                k = 1
                for item in Results:
                    if item.find(",") != -1:
                        f1.write("第" + str(k) + "个可选项：" + item + "\n")
                        split = item.split(",")
                        f2.write(self.product[index]+"——"+str(split[2])+"——"+str(split[3])+",")
                        # f2.write("第" + str(k) + "个可选项,")
                        f2.write(str(split[4])+",")
                        if split[len(split)-1] != str([]):
                            f2.write(str(split[len(split)-1]))
                        else:
                            f2.write(str(split[len(split)-2]))
                        f2.write("\n")
                        k = k + 1
                    else:
                        f1.write(item + "\n")

            else:
                f1.write("系统：该产品不适用该客户！"+"\n")
                print("系统：该产品不适用该客户！")
            index = index + 1

        input("\n"+u"系统：定期寿险产品筛选结束，结果详见Results.txt文件，按任意键结束！")

path = "Results.txt"
f1 = open(path, "w+", encoding='utf-8')
f2 = open("Options.txt", "w+", encoding='utf-8')
First_open = DQSX_System()
First_open.start()
f1.close()
f2.close()