# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 09:40:38 2018

@author: Ben
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

x = np.random.random_integers(-10,10,100)# 隨機產生 100 個在 -10 到 10 之間的整數
y = np.random.random_integers(-10,10,100)# 隨機產生 100 個在 -10 到 10 之間的整數

plt.scatter(x,y)# 畫出散佈圖
plt.show()

X = np.stack((x,y),axis=-1)# 將一維陣列 x 和 y 組成一個二維陣列

"""套件"""
kmeans = KMeans(n_clusters=3)# 分成 3 群
kmeans.fit(X)# 分群

centroids = kmeans.cluster_centers_# 計算群中心
labels = kmeans.labels_# 得到分群標籤
"""套件"""

"""疊代"""
u1 = X[0]# 初始群中心
u2 = X[1]# 初始群中心
u3 = X[2]# 初始群中心
X0 = 0
X1 = 0
X2 = 0
Y0 = 0
Y1 = 0
Y2 = 0
a = 0
b = 0
c = 0

lab = [0] * len(X)

move = 100

while move > 0.001:# 重複直到移動距離小於 0.001
    for j in range(len(X)):
        r1=(X[j][0] - u1[0])**2 + (X[j][1] - u1[1])**2# 距 u1 的距離平方
        r2=(X[j][0] - u2[0])**2 + (X[j][1] - u2[1])**2# 距 u2 的距離平方
        r3=(X[j][0] - u3[0])**2 + (X[j][1] - u3[1])**2# 距 u3 的距離平方
        if r1 == min(r1,r2,r3):# 假如距離 u1 最近
            lab[j] = 0# 分到第一群
            X0 = X0 + X[j][0]# 第一群資料的 X 座標相加
            Y0 = Y0 + X[j][1]# 第一群資料的 Y 座標相加
            a += 1# 第一群的資料個數
        if r2 == min(r1,r2,r3):# 假如距離 u2 最近
            lab[j] = 1# 分到第二群
            X1 = X1 + X[j][0]# 第二群資料的 X 座標相加
            Y1 = Y1 + X[j][1]# 第二群資料的 Y 座標相加
            b += 1# 第二群的資料個數
        if r3 == min(r1,r2,r3):# 假如距離 u3 最近
            lab[j] = 2# 分到第三群
            X2 = X2 + X[j][0]# 第三群資料的 X 座標相加
            Y2 = Y2 + X[j][1]# 第三群資料的 Y 座標相加
            c += 1# 第三群的資料個數
    u1move = (X0/a - u1[0])**2 + (Y0/a - u1[1])**2# u1 移動的距離平方
    u2move = (X1/b - u2[0])**2 + (Y1/b - u2[1])**2# u2 移動的距離平方
    u3move = (X2/c - u3[0])**2 + (Y2/c - u3[1])**2# u3 移動的距離平方
    move = u1move + u2move + u3move# 移動的總距離
    
    u1 = np.array([X0/a, Y0/a])# 更新後的群中心
    u2 = np.array([X1/b, Y1/b])# 更新後的群中心
    u3 = np.array([X2/c, Y2/c])# 更新後的群中心

cent = np.array([u1,u2,u3])# 將群中心存入陣列
"""疊代"""


colors = ["g.","r.","k."]# 綠色、紅色、黑色

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)# 用不同的顏色畫上每個已分群的點
    
plt.scatter(centroids[:, 0],centroids[:,1], marker = "x", s=150, linewidths = 5,zorder = 10)#用 X 標示套件產生的群中心
plt.show()# 顯示圖表


for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[lab[i]], markersize = 10)# 用不同的顏色畫上疊代分群的點
    
plt.scatter(cent[:, 0],cent[:,1], marker = "x", s=150, linewidths = 5,zorder = 10)#用 X 標示疊代產生的群中心
plt.show()# 顯示圖表
