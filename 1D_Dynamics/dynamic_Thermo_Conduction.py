# -*- coding: utf-8 -*-

# 一维非稳态传热计算器
# by: 开环大师; 2020.01.21

# 导入第三方库（轮子s）
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import time

# 物性参数，默认为铁，可以自行修改，公制单位
thermalConductivity = 0.59
specificHeatCapacity = 4.2e3
density = 998
alpha = thermalConductivity / (specificHeatCapacity * density)

# 温度-时间变化率函数（温度数组，空间节点数）：返回该点温度-时间变化率
def tempTimeSlope(Temp, i, alpha, delta_x) :
    a1 = Temp[i-1]
    a2 = Temp[i]
    a3 = Temp[i+1]
    a4 = a1 + a3 - 2*a2
    a5 = alpha * a4
    return a5 / delta_x**2

# 主函数
def main(
    alpha,
    Temp,
    Temp1,
    rodLenth,
    simulationTime,
    spaceSimulationPoint,
    timeSimulationPoint,
    flag = False,
    ) :
    # 计算初始化
    # 设置温度-时间斜率列表，共有 spaceSimulationPoint+2 个节点,两端始终为0
    TempTimeSlope = [0] * (spaceSimulationPoint + 2)
    # 计算空间差分量
    delta_x = rodLenth / (spaceSimulationPoint - 1)
    # 计算时间查分量
    delta_t = simulationTime / (timeSimulationPoint - 1)
    # 生成x列表，用于绘制杆件温度变化图（两侧端点代表环境温度）
    x = [-delta_x]
    for k in range(spaceSimulationPoint + 1) :
        x.append(k*delta_x)

    ''' 生成t列表，绘制温度-时间变化，暂时没用
    t = [-delta_t]
    for k in range(timeSimulationPoint + 1):
        t.append(k*delta_t)
    '''

    # 循环计算，外循环计算时间，内循环计算空间
    for j in range(timeSimulationPoint) :

        for i in range(spaceSimulationPoint):

            if flag == 3 :
                Temp[0] = Temp[1]
                Temp[-1] = Temp[-2]
            elif flag == 2 :
                Temp[-1] = Temp[-2]
            elif flag == 1 :
                Temp[0] = Temp[1]
            else :
                Temp[0] = Temp[0]
                Temp[-1] = Temp[-1]

            TempTimeSlope[i+1] = tempTimeSlope(Temp, i+1, alpha, delta_x)

        DifT = np.array(TempTimeSlope) * delta_t
        Temp = np.array(Temp) + np.array(DifT)

    # 绘制空间温度分布图
    plt.plot(x, Temp, '-.', linewidth = 1)
    plt.xlabel('空间分布 / $m$', color='black')
    plt.ylabel('温度 / $K$', color='black')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.grid(
        b = True, 
        color = 'k', 
        linestyle = '--', 
        linewidth = 1, 
        alpha = 0.5, 
        axis = 'both',
        which = 'major'
        )
    plt.grid(
        b = True, 
        color = 'k', 
        linestyle = '--', 
        linewidth = 0.5, 
        alpha = 0.1, 
        axis = 'both',
        which = 'minor'
        )
    # 把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator = MultipleLocator(0.1*rodLenth)
    x_minor_locator = MultipleLocator(0.01*rodLenth)
    y_major_locator = MultipleLocator(0.2*round(max(Temp1)-min(Temp1)))
    y_minor_locator = MultipleLocator(0.02*round(max(Temp1)-min(Temp1)))
    # ax为两条坐标轴的实例
    ax=plt.gca()
    # 把x/y轴的主刻度设置好
    ax.xaxis.set_major_locator(x_major_locator)
    ax.xaxis.set_minor_locator(x_minor_locator)    
    ax.yaxis.set_major_locator(y_major_locator)
    ax.yaxis.set_minor_locator(y_minor_locator) 
    TargetTemp = Temp1[2]
    # plt.hlines(TargetTemp, 0, rodLenth) # 绘制水平辅助线
    plt.xlim([0, rodLenth]) #指X轴的显示范围
    plt.ylim([10*round(0.09*min(Temp1)), 10*round(0.11*max(Temp1))]) #指y轴的显示范围
    # plt.ylim([min(T1, T2), max(T1, T2)]) #指Y轴的显示范围
    plt.savefig('Graph\\thermoDynamicDiagram.png', dpi = 300, format = 'png')
    # 根据需求决定是否逐帧显示
    # plt.show()

    # 返回温度列表
    return Temp


# 主程序
time1 = time.time()
print('__________________一维非稳态传热计算器__________________')
print('导热材料物性数据需在程序中设定，其他请根据要求写入脚本')
print('更改杆件初始温度分布，需要在程序中更改')
print('使用差分法数值求解，边界条件为环境温度，初始条件为温度分布')
print('若计算结果震荡发散，请尝试降低空间节点数，增加时间节点数')
print('开始计算')

# 设置文件处理
# 文件读取
f1 = open('setup.txt')
w1 = f1.read()
f1.close()
# 按照空字符（含\n）进行逐行分割
w1 = w1.split()

# 初始条件文件处理
# 文件读取
f2 = open('initialState.txt')
w2 = f2.read()
f2.close()
# 按照空字符（含\n）进行逐行分割
w2 = w2.split(',')
lenth1 = len(w2)
# 建立初始温差列表,首项/末项为环境温度差变量，均为0
# 首项温度差为0
iniT = [0]

# 将字符串转化为数值列表,即初始温差列表（从左向右）
for i in range(lenth1) :
    delT = eval(w2[i])
    init = iniT.append(delT)

# 初始化标志变量
a1 = 0
# 主循环
for lst in w1 :
    # 逐行读取控制脚本
    ctr = lst.split(',')
    # 脚本数值化，传参
    T0 = eval(ctr[0])
    T1 = eval(ctr[1])
    T2 = eval(ctr[2])
    rodLenth = eval(ctr[3])
    simulationTime = eval(ctr[4])
    spaceSimulationPoint = eval(ctr[5])
    timeSimulationPoint = eval(ctr[6])
    # 生成温度列表，杆上有spaceSimulationPoint个节点，两端再加两个节点代表环境温度
    Temp = [T0] * (spaceSimulationPoint + 2)
    # 设置两侧环境温度
    Temp[0] = T1
    Temp[-1] = T2
    # 计算温差补齐函数长度
    lenth2 = spaceSimulationPoint - lenth1 + 1
    initialT = iniT + [0]*lenth2
    # 加上初始温差分布
    Temp = np.array(Temp) + np.array(initialT)
    # 记录下初始温度分布，确定坐标值
    a1 = 1 + a1
    if a1 == 1 :
        Temp1 = Temp
        # 特殊情况，可以在Temp1中手动输入温度坐标上限/下限，如：
        # 第三项为水平辅助线温度值，默认0
        Temp1 = [280, 380, 363]

    # 判断是否为绝热杆，定义标志位
    if T1 == 0 :
        if T2 == 0 :
            flag = 3    # 两侧绝热
        else :
            flag = 1    # 左侧绝热
    else :
        if T2 == 0 :
            flag = 2    # 右侧绝热
        else :
            flag = 0    # 不绝热

    # 调用主函数
    main(
        alpha,
        Temp,
        Temp1,
        rodLenth,
        simulationTime,
        spaceSimulationPoint,
        timeSimulationPoint,
        flag, # 标志位，0时两端不绝热，1时左端绝热，2时右端绝热，3时两侧绝热
        )
    # 检修程序时建议break一下，要不太慢
    # break
time2 = time.time()
# 结束提示
print('程序执行完毕，共 ', round(time2-time1, 1), ' 秒')
