from matrix import D_100
import time

D = D_100
N = 100
MAX = 99999

for i in range(N):
    D[i][i] = MAX

city_list = [0]
gub_visited = [False]*N
gub_visited[0] = True

def get_upper_bound(city_temp,city_num,path_length):
    if city_num == N-1:
        return path_length + D[city_temp][0]
    min_length = MAX
    p=0
    for i in range(N):
        if gub_visited[i]==False and min_length>D[city_temp][i]:
            min_length = D[city_temp][i]
            p = i
    city_list.append(p)
    gub_visited[p] = True
    return get_upper_bound(p, city_num+1, path_length + min_length)

start_time = time.time()
length = get_upper_bound(0,0,0)
city_list.append(0)

print('算法运行总时间为：{:.4f}'.format(time.time()-start_time))
print('经过城市的顺序为:',city_list)
print('经过的总距离为：{:.2f}'.format(length))