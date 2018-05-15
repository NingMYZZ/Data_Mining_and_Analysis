import numpy as np

file = open('./iris.txt')
lines =file.readlines()
data_list=[]
for line in lines:
    temp=line.split(',')
    if '"Iris-versicolor"\n' in temp:
       temp.remove('"Iris-versicolor"\n')
    elif '"Iris-virginica"\n' in temp:
        temp.remove('"Iris-virginica"\n')
    elif '"Iris-setosa"\n'in temp:
        temp.remove('"Iris-setosa"\n')
    data_list.append(temp)
data=np.matrix(data_list)
data=data.astype(float)                             # this is the original data
#*********************************************** one **********************************
K_matrix=np.power(data.T*data,2)

#******************************************* two **************************************************

data_x=[]                                            #通过叉积计算
for i in data:
    temp=np.power(i,2)
    data_x.append(temp)
data=np.array(data)

data_y=[]
for i in range(0,data.shape[1]):                    #将点投射到特征空间
    temp = []
    for j in range(0,data.shape[0]):
        currnet=j+1
        while currnet<=data.shape[0]-1:
            temp.append(np.sqrt(2)*data[j][i]*data[currnet][i])
            currnet=currnet+1
    data_y.append(temp)

data_x=np.array(data_x)
data_y=np.array(data_y)

data_x.shape=[150,4]
data_y=data_y.T

data_k_fea=np.vstack((data_x,data_y))
data_k_fea=np.matrix(data_k_fea)                    #feature space

data_k = data_k_fea.T*data_k_fea                    #k matrix

data_k_means=np.mean(data_k,axis=1)                 #means per row
data_k_centered=data_k-data_k_means

data_k_std=np.std(data_k,axis=1)
data_k_normal=[]

for (i1, i2) in zip(data_k_centered,data_k_std):
    temp=i1/i2
    data_k_normal.append(temp)

data_k_normal=np.array(data_k_normal)
data_k_normal=np.matrix(data_k_normal)

print data_k_centered
print data_k_normal