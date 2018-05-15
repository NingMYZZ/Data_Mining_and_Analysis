# -*- coding: cp936 -*-
import numpy as np
import scipy
import matplotlib.pyplot as plt
import sys

from scipy import stats

f=open("./magic04.txt")
lines=f.readlines()
data_list=[]
for line in lines:
    temp = line.split(',')
    if 'g\n' in temp:
        temp.remove('g\n')
    elif  'h\n' in temp:
        temp.remove('h\n')
    data_list.append(temp)
data = np.array(data_list)
data = data.astype(float)                              # this is original data
#******************************** one ************************************************

data_mena=np.mean(data,axis=0)                         #计算均值

#******************************** two and three************************************************
data_cented=[]                                         #cented data
for i in data:
    temp=i-data_mena
    data_cented.append(temp)

data_cented=np.array(data_cented)
data_cented_T=data_cented.T

n=data_cented.shape[0]

data_cented=np.matrix(data_cented)
data_cented_T=np.matrix(data_cented_T)


data_cova1=(data_cented_T*data_cented)//n               #通过列之间的內积计算样本协方差矩阵
data_cova2=[[0 for x in range(10)] for y in range(10)]

for i in data_cented:                                   #cross product
    #i.shape=(10,1)
    temp= np.transpose(i)
    num=(temp*i)
    data_cova2=data_cova2+num

data_cova2=data_cova2//n

#************************************ four ***********************************************************
a=data[:,0]                                           #Attribute 1  this must the data,but not ccented
b=data[:,1]                                           #Attribute 2
L_a=np.sqrt(a.dot(a))
L_b=np.sqrt(b.dot(b))
cos_angle=a.dot(b)/(L_a*L_b)                          #cosine of the angle


p1=plt.scatter(a,b)
plt.title('Scatter')
plt.legend(loc = 'upper right')
plt.show()


#************************************ five ***************************************************************

std=np.std(a)                                         # fang ca
mean1=np.mean(a)                                    # means

u=mean1
sig=std

plt.title('Normal:$\mu$=%.1f,$\sigma^2$=%.1f' % (mean1,sig))
plt.xlabel('x')
plt.ylabel('probability density')

x = np.linspace(u - 3 * sig, u + 3 * sig, 50)
y_sig = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (np.math.sqrt(2 * np.math.pi) * sig)
plt.plot(x, y_sig, "r-", linewidth=2)
plt.grid(True)
plt.show()


#********************************* six *******************************************************
data_std=np.std(data,axis=0)
data_var=np.var(data,axis=0)

max_std=0.0
min_std=data_std[0]
for i in data_std:
    if i>max_std:
        max_std=i
    if i<min_std:
        min_std=i


#*********************************** seven *******************************************************
data_cova1=np.array(data_cova1)
max_cov=0.0
min_cov=data_cova1[0][0]                            #data_cova1 is the sample covariance matrix
for i in data_cova1:
    for j in i:
        if j>max_cov:
            max_cov=j
        if j<min_cov:
            min_cov=j

print max_cov
print min_cov