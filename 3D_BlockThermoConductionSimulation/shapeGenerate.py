import numpy as np
import time
import copy

class Glob:  # 球体类

    def __init__(self):    # 实例化后自身变量
        # 注：本体与模拟空间的边界至少存在1个模拟微元的间隔
        self.sizex = 100  # 模拟空间x方向尺寸
        self.sizey = 100  # 模拟空间y方向尺寸
        self.sizez = 100  # 模拟空间z方向尺寸
        self.R = 45       # 本体球体半径
        self.Tsur = 373   # 环境温度
        self.Tbar = 273   # 本体温度
        # 生成一个模拟空间形状的全 0 的三维数组，并将其整形为需要的立方空间
        self.StructureArr = np.zeros(self.sizez*self.sizey*self.sizex).reshape(self.sizez, self.sizey, self.sizex)
    
    # 形体矩阵内部绘制
    def insideStructure(self):
        # 勾股定理，循环计算，判断是否为求体内点
        # 球体的点赋予 2 进行标记
        l = round(self.sizex / 2)
        m = round(self.sizey / 2)
        n = round(self.sizez / 2)
        for k in range(self.sizez):
            for j in range(self.sizey):
                for i in range(self.sizex):
                    self.r = (i - l)**2 + (j - m)**2 + (k - n)**2
                    if self.r <= self.R**2 :
                        self.StructureArr[k][j][i] = 2

    # 形体边界
    def boundaryStructure(self):
        # 与本体相邻的即为边界
        # 球体的点边界点赋予 1 进行标记
        for k in range(1, self.sizez-1):
            for j in range(1, self.sizey-1):
                for i in range(1, self.sizex-1):
                    if self.StructureArr[k][j][i+1] == 2 and self.StructureArr[k][j][i-1] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j][i-1] == 2 and self.StructureArr[k][j][i+1] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j+1][i] == 2 and self.StructureArr[k][j-1][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j-1][i] == 2 and self.StructureArr[k][j+1][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k+1][j][i] == 2 and self.StructureArr[k-1][j][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k-1][j][i] == 2 and self.StructureArr[k+1][j][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    else :
                        self.StructureArr[k][j][i] = self.StructureArr[k][j][i]

    # 将形体矩阵的值转化为对应温度分布
    def Temp(self):
        # 深拷贝一个形体矩阵，即：温度分布矩阵
        self.TempArr = copy.deepcopy(self.StructureArr)
        # 将拷贝后的形体矩阵按照标记是边界点、体点进行赋值，赋予边界温度于球体本身的温度
        self.TempArr[self.TempArr == 2] = self.Tbar
        self.TempArr[self.TempArr == 1] = self.Tsur

    # 返回温度分布结果（即：温度分布矩阵）
    def resultTemp(self):
        return self.TempArr

    # 返回形体矩阵结果
    def resultStructure(self):
        return self.StructureArr

if __name__ == '__main__':
    
    print('\n', 10*'-', '开始构建计算矩阵', 10*'-')

    t1 = time.time()            # 计时模块

    S = Glob()                  # 对象实例化
    S.insideStructure()         # 构建仿真物体的离散空间结构
    S.boundaryStructure()       # 构建离散物体的边界点
    S.Temp()                    # 生成仿真空间的温度分布

    M1 = S.resultTemp()         # 获取 np 数组形式的温度矩阵
    M2 = S.resultStructure()    # 获取 np 数组形式的形体矩阵

    np.set_printoptions(threshold=np.inf)

    np.save('Data\\Tdistribution.npy', M1)      # 保存温度分布矩阵
    np.save('Data\\Structure.npy', M2)          # 保存形体矩阵

    t2 = time.time()                            # 计时模块

    print('\n结构文件产生完毕，耗时：{:.3f}s'.format(t2 - t1))
