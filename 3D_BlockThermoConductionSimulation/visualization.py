import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# 载入数据
Tdistribution = np.load('Data\\TdistributionRes.npy')
Guide = np.load('Data\\Guide.npy')
# 数据格式化，对非本体进行遮罩，非本体部分重置为0，以区分本体与环境
Tdistribution = np.array(Tdistribution) * np.array(Guide)

# 输出中心温度
i = round(Tdistribution.shape[2])
j = round(Tdistribution.shape[1])
k = round(Tdistribution.shape[0])
print('\n物体中心温度为：', round(Tdistribution[round(k/2)][round(j/2)][round(i/2)]), 'K')

# 初始化参数
sns.set()

# 四张子图
fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows = 2, ncols=2, figsize=(6.2,5)) # 子图结构与尺寸
fig.subplots_adjust(wspace = 0.25, hspace = 0.25)   # 子图间隔 

# 绘图设置
heatmap1 = sns.heatmap(
    Tdistribution[round(0.125*k)], 
    vmin=273, vmax = 373, annot_kws = {"size": 10}, 
    annot = False, 
    fmt = '.1f', 
    linewidths = 0.0, 
    ax = ax1, 
    cmap = cm.coolwarm,
    
    )    # 1/8 截面

heatmap2 = sns.heatmap(
    Tdistribution[round(0.25*k)], 
    vmin=273, vmax = 373, annot_kws = {"size": 10}, 
    annot = False, 
    fmt = '.0f', 
    linewidths = 0.0, 
    ax = ax2, 
    cmap = cm.coolwarm
    )    # 1/4 截面

heatmap3 = sns.heatmap(
    Tdistribution[round(0.375*k)], 
    vmin=273, vmax = 373, 
    annot_kws = {"size": 10}, 
    annot = False, 
    fmt = '.0f', 
    linewidths = 0.0, 
    ax = ax3, 
    cmap = cm.coolwarm
    )    # 3/8 截面

heatmap4 = sns.heatmap(
    Tdistribution[round(0.5*k)], 
    vmin=273, 
    vmax = 373, 
    annot_kws = {"size": 10}, 
    annot = False, 
    fmt = '.0f', 
    linewidths = 0.0, 
    ax = ax4, 
    cmap = cm.coolwarm
    )    # 1/2 截面

plt.savefig('Graph\\Result.png', dpi = 300)
plt.show()

print('\n可视化过程结束，图片已保存\n')