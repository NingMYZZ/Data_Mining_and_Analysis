# -*- coding: cp936 -*-
from collections import Counter
from numpy import *
import numpy as np
import sys
sys.setrecursionlimit(1000000)

data = np.loadtxt("./iris.txt", delimiter=',', usecols=(0, 1, 2, 3), dtype=float)
label = np.loadtxt("./iris.txt", delimiter=',', usecols=(range(4, 5)), dtype=str)
c=set(label)
c=list(c)

data=data.tolist()
label=label.tolist()

for i in range(len(data)):
    data[i].append(label[i])

Data_Node=[]

def spilitdata(D,v,X):                               #按照分割点将数据分割成两部分
    Dy=[]
    Dn=[]
    for i in range(len(D)):
        if(D[i][X] >=v):
            Dy.append(D[i])
        else:
            Dn.append(D[i])
    return Dy,Dn


def EVALUATE_NUMERIC_ATTRIBUTE(D,X):
    D = sorted(D, key=lambda x:x[X])
    M=set()                                                 #分割点
    N={}
    n=[0.0 for i in range(0,len(c))]
    for j in range(len(D)-1):
        for i in range(0,len(c)):
            if (D[j][-1]==c[i]):
                n[i]=n[i]+1
        if (D[j][X]!=D[j+1][X]):
            v=(D[j][X]+D[j+1][X])/2
            M.add(v)
            N[v]=[0.0 for i in range(len(c))]
            temp=[]
            for i in range(0,len(c)):
                if D[j][X]<=v :
                    N[v][i]=n[i]
    for i in range(0,len(c)):
        if (D[len(D)-1][-1]==c[i] ):
            n[i]=n[i]+1

    point=0.0                                         #分割点
    value=0.0                                         #分值
    for v in M:
        Py=[0.0 for i in range(len(c))]
        Pn=[0.0 for i in range(len(c))]
        for i in range(len(c)):
            temp=0.0
            for j in range(len(c)):
                temp=temp+N[v][j]
            temp1=0.0
            for j in range(len(c)):
                temp1=temp1+n[j]-N[v][j]
            Py[i]=N[v][i]/temp
            Pn[i]=(n[i]-N[v][i])/temp1
        nd=len(D)
        ny=0.0
        nn=0.0

        for i in range(len(D)):
            if (D[i][X] <= v):
                ny=ny+1
            else:
                nn=nn+1
        h=0.0
        h1=0.0
        h2=0.0
        for i in range(len(c)):                     #H(DY,DN)
            if Py[i]!=0.0:
                h1=h1-Py[i]*np.math.log(Py[i],2)
            if Pn[i]!=0.0:
                h2=h2-Pn[i]*np.math.log(Pn[i],2)
        h3=calentropy(D,c)                          #H(D)
        h=h3-((ny/nd)*h1+(nn/nd)*h2)
        if h>value:
            value=h
            point=v

    return value,point

def calentropy(D,c):
    h=0.0
    number =[0.0 for i in range(len(c))]
    for j in range(len(D)):                             #统计每个类别出现的个数
        for i in range(len(c)):
            if(D[j][-1]==c[i]):
                number[i]=number[i]+1
    for i in range(len(c)):
        p1=number[i]/len(D)
        p2=0.0
        if p1 !=0.0:
            p2=np.math.log(p1,2)
        h=h - p1*p2
    return h

def DECISIONTREE(D,p,q):                                    #p叶子大小的阈值，q叶子密度阈值
    n=len(D)
    ni = {}
    for i in range(len(D)):
        ni[D[i][-1]] = ni.get(D[i][-1], 0) + 1
    purity_D=max(ni.values())/n

    if n<=p or purity_D>=q:
        c= np.argmax(ni)
        Data_Node.append(D)
        return D
    value = 0                                               # 分值信息增益
    point = 0                                               # 分割点,大于point左边，小于->右边
    maxAttri = 0                                            # 分割的属性
    for attri in range(len(D[0])-1):
        temValue,temPoint=EVALUATE_NUMERIC_ATTRIBUTE(D,attri)
        if temValue>value:
            value=temValue
            point=temPoint
            maxAttri=attri

    print point,maxAttri

    Dy=[]
    Dn=[]
    Dy,Dn=spilitdata(D,point,maxAttri)
    DECISIONTREE(Dy, p, q)
    DECISIONTREE(Dn, p, q)


DECISIONTREE(data,5,0.95)


for i in range(0,len(Data_Node)):
    number =[0.0 for m in range(len(c))]
    for j in range(len(Data_Node[i])):                             #统计每个类别出现的个数
        for k in range(len(c)):
            if(Data_Node[i][j][-1]==c[k]):
                number[k]=number[k]+1

    print max(number)/len(Data_Node[i])
