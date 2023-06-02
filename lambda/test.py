import numpy as np

# 创建一个1维数组
a = np.array([1, 2, 3, 4, 5])
print(a)

# 创建一个2维数组
b = np.array([[1, 2, 3], [4, 5, 6]])
print(b)

# 访问数组元素
print(a[0])  # 输出第一个元素
print(b[1, 2])  # 输出第二行第三列的元素

# 数组运算
c = a + b  # 对应元素相加
print(c)

d = np.dot(a, b)  # 矩阵乘法运算
print(d)

# 数组函数
e = np.sin(a)  # 求正弦值
print(e)

f = np.mean(b)  # 求平均值
print(f)