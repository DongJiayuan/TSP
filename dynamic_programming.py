import numpy as np
from itertools import combinations
from matrix import D_10
import time
#动态规划解决旅行商问题
#Held–Karp algorithm
'''
function algorithm TSP (G, n)
  for k := 2 to n do
    C({k}, k) := d1,k
  end for

  for s := 2 to n-1 do
    for all S ⊆ {2, . . . , n}, |S| = s do
      for all k ∈ S do
        C(S, k) := minm≠k,m∈S [C(S\{k}, m) + dm,k]
      end for
    end for
  end for

  opt := mink≠1 [C({2, 3, . . . , n}, k) + dk,1]
  return (opt)
end
'''

#D(i,j){i>j}为从i到j的距离
#D(j,i){i<j}为从j到i的距离
D = D_10
N = 10 #城市个数
MAX = 99999
#横坐标为已经过城市的二进制值，纵坐标为当前最后经过的城市
#原点不包括在内


C = MAX * np.ones([2**(N-1),N-1]) #最短路径值矩阵
path = MAX * np.zeros([2**(N-1),N-1],dtype=np.int) #路径矩阵

#在S集合中任取num个元素，返回所有可能结果组成的列表
def get_set_element(S,num):
     x = []
     for i in combinations(S,num):
          x.append(set(i))
     return x

#把集合转化成二进制数
def element_to_vector(element_set):
     vector = 0
     for i in element_set:
          vector = vector | 1<<i
     return vector

start = time.time()
city_set = set()
for i in range(N-1): #不包括city0
     city_set.add(i)

#从集合到字典：字典的key为取的元素个数，对应的value为相应个数的元素组合
set_dict = {}
for i in range(1,N):
     set_dict[str(i)] = get_set_element(city_set,i)

#city0(start point),city1,...,city N-1
for i in range(N-1): #开始计算第一个城市
     #第i+1个city
     reached_set = 0 | 1<<i
     C[reached_set][i] = D[0][i+1]

for i in range(2,N): #开始计算第i+1个城市
     past_city = set_dict[str(i)] #i+1个城市的组合
     for j in past_city:
          city_vector = element_to_vector(j)
          for k in j:
               old_city_vector = city_vector ^ 1<<k
               for m in j:
                    if m != k:
                         dis = C[old_city_vector][m]+D[m+1][k+1]
                         if dis < C[city_vector][k]:
                             C[city_vector][k] = dis
                             path[city_vector][k] = m

#找到到达原点前经过的那个城市
final_dis = C[element_to_vector(city_set)][0]+D[1][0]
city_last = 0
for k in range(1,N-1):
     dis = C[element_to_vector(city_set)][k]+D[k+1][0]
     if dis < final_dis:
         final_dis = dis
         city_last = k


#get path
path_list = [-1,city_last]
index1 = element_to_vector(city_set)
before_k = path[index1][city_last]
path_list.append(before_k)
for i in range(N-3):
     index1 = index1 ^ 1<<city_last
     city_last = before_k
     before_k = path[index1][city_last]
     path_list.append(before_k)
path_list.append(-1)

for i in range(len(path_list)):
     path_list[i] +=1

final_path = path_list.reverse()

print('算法运行总时间为：{:.4f}'.format(time.time()-start))
print('经过城市的顺序为:',path_list)
print('经过的总距离为：{:.2f}'.format(final_dis))



