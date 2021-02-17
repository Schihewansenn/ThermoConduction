import os
import time
print("各向同性介质均一非稳态非稳态传热仿真计算器")

t1 = time.time()
# 输出说明
with open('Setup\\readme.txt','r', encoding='UTF-8' ) as file:
    words = file.read()
print(words, '\n')

# 修改程序
par1 = input('设计结构请输入1，设计输入可视化请输入2，直接计算请输入3（建议先配置再选 3）:\n')
if par1 == '1' :
    os.system('shapeGenerate.py')
elif par1 == '2' :
    os.system("visualization.py")
else :
    print('即将开始计算，正在加载数据')
    # 调用程序脚本计算
    os.system('python shapeGenerate.py')
    os.system('python 3D_5.py')
    print('正在进行结果可视化，即将输出结果')
    os.system('python visualization.py')
    t2 = time.time()

print('程序运行结束，结果已保存')
print('总程序共用时', round(t2-t1), 's')
