import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from mpl_toolkits.mplot3d import Axes3D
 
print(321)
def Fun(x,y,p):                        # 定义拟合函数形式
    a1,a2,a3 = p
    return a1*x+a2*y+a3

def error (p,x,y,z):                    # 拟合残差
    return Fun(x,y,p)-z 

x = []
y = []
z = []
with open("./fac_data.txt","r") as f:
    for line in f:
        a1,a2,a3 = line[0:-1].split('\t')
        # print(a1," ",a2," ",a3)
        x.append(int(a1))
        y.append(int(a2))
        z.append(int(a3))
x = np.array(x)
y = np.array(y)
z = np.array(z)
# print(x)
# p_value = [-2,5,10] # 原始数据的参数
# noise = np.random.randn(len(x))  # 创建随机噪声
# y = Fun(p_value,x)+noise*2 # 加上噪声的序列
p0 = [0.1,-0.01,100] # 拟合的初始参数设置
para =leastsq(error, p0, args=(x,y,z)) # 进行拟合
a,b,c = para[0]

print("z=",str(a),"x + ",str(b),"y + ",str(c))

xp = np.linspace(-1,6,100)
yp = np.linspace(-1,6,100)

X,Y = np.meshgrid(xp,yp)
Z = Fun(X,Y,[a,b,c])

fig = plt.figure()

ax = Axes3D(fig)

ax.plot_surface(X, Y, Z, alpha=0.5)
ax.scatter(x,y,z,color="r")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()
# y_fitted = Fun (para[0],x) # 画出拟合后的曲线

# plt.figure
# plt.plot(x,y,'r', label = 'Original curve')
# plt.plot(x,y_fitted,'-b', label ='Fitted curve')
# plt.legend()
# plt.show()
# print (para[0])
