# -*- coding: cp936 -*-
from collections import Counter

import  numpy as np
import math
import matplotlib.pyplot as plt
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

file=open('./iris.txt')
lines =file.readlines()
data_list=[]
for line in lines:
    temp=line.split(',')
    if '"Iris-versicolor"\n' in temp:
       #temp.remove('"Iris-versicolor"\n')
        temp[-1]='0'
    elif '"Iris-virginica"\n' in temp:
        #temp.remove('"Iris-virginica"\n')
        temp[-1]='1'
    elif '"Iris-setosa"\n'in temp:
        #temp.remove('"Iris-setosa"\n')
        temp[-1]='2'
    data_list.append(temp)

data=[]
for i in data_list:
    i=map(eval,i)
    data.append(i)

def dis(a,b):                                       #计算距离
    a=np.array(a)
    a=a.astype(float)
    b=np.array(b)
    b=b.astype(float)
    s=0.0
    for i in range(len(a)-1):                       #最后一列表示类别，不参与计算
        s=s+np.power(a[i]-b[i],2)
    return np.sqrt(s)

def N(a,D,e):                                       #计算距离小于e的个数
    n=0
    for i in D:
        if(dis(a,i)<=e):
            n=n+1
    return n

def CorePoint(T,D,e,minpts):                        #计算得到 core point
    for i in D:
        if N(i,D,e)>=minpts:
            T.append(i)

def K(z):
    d=z.shape[1]                                    # z是一个行向量，矩阵的列，注意这里跟PPT的区别
    m=(-(z*z.T)/2).tolist()
    n=m[0][0]
    k=np.power(math.e, n)/(np.power(2*math.pi,d/2))
    return k

def mea(x,D,h):                                     #x的更新
    temp1 = 0
    temp2 = 0
    x=np.matrix(x)
    for i in D:
        i=i[0:4]
        i=np.matrix(i)
        temp1=temp1+K((x-i)/h)*i
        temp2=temp2+K((x-i)/h)
    result=(temp1/temp2).tolist()
    return result[0]                                #返回一个list

def FindAtt(x,D,h,e):
    t=0
    num=[]
    num.append(x[0:4])                             #最后一列是属性，不参与计算
    while(1):
        temp=mea(num[t],D,h)
        num.append(temp)
        t=t+1
        if(dis(num[t],num[t-1]) <= e):
            return num[t]

def f(x,h,D):                                       #x是list,密度估计
    D=np.matrix(D)
    D=D.astype(float)
    x=np.matrix(x)
    x=x.astype(float)
    n=D.shape[0]                                    #向量的个数
    d=x.shape[1]                                    #向量的维度
    temp=0


    for i in D:
        i=i[0,0:4]
        temp=temp+K((x-i)/h)
    temp=temp/(n * np.power(h,d))
    temp =temp.tolist()

    return temp                                     #这里要返回一个数，

def Scan(D,e,minpts):
    P=D
    k = 0                                               # number of classes
    C=[]
    T = []
    CorePoint(T,D,e,minpts)                            #T中是core point

    while(len(T)):
        P_old=P
        o=list(T)[np.random.randint(0,len(T))]
        P = [i for i in P if i!=o]
        Q = [];
        Q.append(o)
        while len(Q):
            q = Q[0]
            Nq = [i for i in D if dis(q, i) <= e]                          #所有满足在i的e范围的点
            if len(Nq) >= e:
                S = [v for v in P if v in Nq]                              #交集，
                Q+=S
                P = [d for d in P if d not in S]                           #P里面需要除去这些已经计算的点
            Q.remove(q)
        k += 1
        Ck = [m for m in P_old if m not in P]                             #刚才的那一类
        T=[s for s in T if s not in Ck]                                   #T=T-Ck
        C.append(Ck)
    return C

def DENCLUE(D,h,min,e):                         #min密度阈值，e是来计算收敛,若 h=最小距离，min等于minpts，则跟dbscan一样
    A=[]
    R=[]
    C=[]
    finded=bool(0)                              #是否找到
    for i in D:
        temp=FindAtt(i,D,h,e)                   #密度索引
        if(f(temp,h,D)>=min):
            A.append(temp)                      #存放x attractor
            finded=1
            while(finded!=0):
                for j in range(0,len(R)):       #先查找存不存在这个密度索引，如果存在直接插入
                    if(R[j][0]==temp):
                        R[j].append(i)
                        finded=0                #找到这个密度索引，插入i，置为1
                if(finded==1):                  #若不存在这个索引，插入之后在循环一遍
                    cur=[]
                    cur.append(temp)
                    R.append(cur)
    c=Scan(A,h,5)

    for i in c:
        temp = []
        for j in i:                             #j是attractor,i包含的所有向量，都是直接密度可达
            for m in range(0, len(R)):          #遍历找j，所在的行
                if (R[m][0] == j):
                    del R[m][0]
                    temp=temp+R[m]
                    break
        C.append(temp)

    return C

clustrs=DENCLUE(data,0.2,0.08,0.0001)


chu=[[0.0for i in range(4)] for j in range(8)]                       #最后一列存放纯度
for i in range(len(clustrs)):
    for j in range(len(clustrs[i])):
        chu[i][clustrs[i][j][-1]]=chu[i][clustrs[i][j][-1]]+1
    chu[i][-1]=max(chu[i])/len(clustrs[i])


C=clustrs


for i in range(len(chu)):
    print chu[i][-1]
    print ' '


print  clustrs
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for i in range(len(C)):
#     X = []
#     Y = []
#     Z = []
#     for j in range(len(C[i])):
#         X.append(C[i][j][0])
#         Y.append(C[i][j][1])
#         Z.append(f(C[i][j],0.2,data))
#     ax.plot_trisurf(X, Y, Z)
# pl.show()




