import numpy as np
import math

def Norm2(a,b):
    dist_2 = (a[0]-b[0])**2 + (a[1]-b[1])**2
    dist = math.sqrt(dist_2)
    return dist

citylist1 = []
with open('TSP10cities.tsp') as f:
    for line in f.readlines():
        x = line[:-1].split(' ')
        coordinate = (int(x[1]),int(x[2]))
        citylist1.append(coordinate)

N = len(citylist1)
D_10 = np.zeros([N,N])
for i in range(N):
    for j in range(N):
        D_10[i][j] = Norm2(citylist1[i],citylist1[j])

citylist2 = []
with open('TSP100cities.tsp') as f:
    for line in f.readlines():
        x = line[:-1].split(' ')
        coordinate = (int(x[1]),int(x[2]))
        citylist2.append(coordinate)

N = len(citylist2)
D_100 = np.zeros([N,N])
for i in range(N):
    for j in range(N):
        D_100[i][j] = Norm2(citylist2[i],citylist2[j])



