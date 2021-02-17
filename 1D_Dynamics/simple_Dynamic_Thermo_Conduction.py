# 一维非稳态传热计算器
# by: 开环大师; 2020.01.21

# 导入第三方库（轮子s）
import numpy as np
import matplotlib.pyplot as plt

# 物性参数，默认为铁，可以自行修改，公制单位
thermalConductivity = 45
specificHeatCapacity = 460
density = 7900
alpha = thermalConductivity / (specificHeatCapacity * density)

# 温度-时间变化率函数（温度数组，空间节点数）：返回该点温度-时间变化率
def tempTimeSlope(Temp, i, alpha, delta_x):
    a1 = Temp[i-1]
    a2 = Temp[i]
    a3 = Temp[i+1]
    a4 = a1 + a3 - 2*a2
    a5 = alpha * a4 /2
    return a5 / delta_x**2

print('__________________一维非稳态传热计算器__________________')
print('导热材料物性数据需在脚本中设定，其他请根据需要输入')
print('生成的温度分布图两端端点代表两侧环境温度，而非杆件温度')
print('更改杆件初始温度分布，需要在脚本中更改')
print('使用差分法数值求解，边界条件为环境温度，初始条件为温度分布')

# 初始状态与边界条件，初始状态默认杆件恒温分布，可以修改
T0 = eval(input('请输入初始恒定温度(K) = '))
T1 = eval(input('请输入左端环境温度(K) = '))
T2 = eval(input('请输入右端环境温度(K) = '))

# simulation setup
rodLenth = eval(input('请输入杆件长度(m) = '))
simulationTime = eval(input('请输入模拟时间(s) = '))
print('建议空间节点数目 = 10个/dm')
print('建议时间节点个数 = 2个/ s')
spaceSimulationPoint = eval(input('请输入空间节点数目（微元尺寸 > 0.01m） = '))
timeSimulationPoint = eval(input('请输入时间节点数目（模拟时间 < 1s） = '))
print('若计算结果震荡发散，请尝试降低空间节点数，增加时间节点数')

# 计算初始化
# 生成温度列表，杆上有spaceSimulationPoint个节点，两端再加两个节点代表环境温度
Temp = [T0] * (spaceSimulationPoint + 2)
# 设置两侧环境温度
Temp[0] = T1
Temp[-1] = T2
# 还可参照上面的方法设置初始温度分布（可选）
# 设置温度-时间斜率列表，共有 spaceSimulationPoint+2 个节点,两端始终为0
TempTimeSlope = [0] * (spaceSimulationPoint + 2)
# 计算空间差分量
delta_x = rodLenth / (spaceSimulationPoint - 1)
# 计算时间查分量
delta_t = simulationTime / (timeSimulationPoint - 1)
# 生成x列表，用于绘制杆件温度变化图（两侧端点代表环境温度）
x = [-delta_x]
for k in range(spaceSimulationPoint + 1):
    x.append(k*delta_x)

''' 生成t列表，绘制温度-时间变化，暂时没用
t = [-delta_t]
for k in range(timeSimulationPoint + 1):
    t.append(k*delta_t)
'''

# 循环计算，外循环计算时间，内循环计算空间
for j in range(timeSimulationPoint):
    for i in range(spaceSimulationPoint):
        TempTimeSlope[i+1] = tempTimeSlope(Temp, i+1, alpha, delta_x)
    DifT = np.array(TempTimeSlope) * delta_t
    Temp = np.array(Temp) + np.array(DifT)

# 绘制空间温度分布图
plt.plot(x, Temp, '-+')
plt.xlabel('Space scale')
plt.ylabel('Temperature / K')
plt.savefig('Graph\\simple_ThermoDynamic_Simulation.png', dpi=300)
plt.show()

# 结束提示
print('程序结束')