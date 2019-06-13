from queue import PriorityQueue as PQueue
from matrix import D_100
import time

D = D_100
N = 100
MAX = 99999

for i in range(N):
    D[i][i] = MAX

#每个结点代表暂时确定的路径
class Node:
    #参数列表为参观过城市的标记、起点、终点、经过的城市数、目标函数值、当前路径
    def __init__(self,visited,start,end,k,length,lb,city_list):
        self.visited = visited
        self.start = start
        self.end = end
        self.k = k
        self.length = length
        self.lb = lb
        self.city_list = city_list

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
    gub_visited[p] = True
    return get_upper_bound(p, city_num+1, path_length + min_length)

#计算当前路径p的目标函数
def get_lb(p):
    pre_length = p.length*2
    min1 = MAX
    min2 = MAX
    #所有可行的进入起点的边中找一条最小的
    for i in range(N):
        if p.visited[i]==False and min1>D[i][p.start]:
            min1=D[i][p.start]
    pre_length = pre_length + min1
    
    #所有可行的从重点出发的边中找一条最小的
    for j in range(N):
        if p.visited[j]==False and min2>D[p.end][j]:
            min2 = D[p.end][j]
    pre_length = pre_length + min2

    #求要经过未遍历的城市中的路径的下界
    for i in range(N):
        if p.visited[i]==False:
            min1 = MAX
            min2 = MAX
            for j in range(N):
                min1=D[i][j] if min1 > D[i][j] else min1
            for m in range(N):
                min2=D[m][i] if min2 > D[m][i] else min2
            pre_length = pre_length + min1 + min2
    return pre_length/2

start_time = time.time()
up = get_upper_bound(0,0,0)

pq = PQueue() #创建一个优先队列

visited = [False]*N
visited[0] = True
#初始点的lb不起作用，因此随便赋值为0
node = Node(visited=visited,start=0,end=0,k=1,length=0,lb=0,city_list=[0])

index = 0
pq.put((node.lb,index,node)) #将起点加入队列
while pq.qsize()!=0:
    tmp = pq.get()[2]
    if tmp.k==N-1:
        #找到最后一个要经过的点
        for i in range(N):
            if tmp.visited[i]==False:
                p = i
                break
        #根据当前最小lb节点得到的一条完整路径长度
        whole_length = tmp.length + D[tmp.end][p] + D[p][tmp.start]
        #如果当前的路径和比当前最小下界都小则跳出
        #否则继续求其他可能的路径，并更新上界
        if whole_length <= pq.get()[0]:
            tmp.city_list.append(p)
            break
        elif whole_length <= up:
            #记录当前得到的最短完整路径的节点（并记录最后一个经过的城市）
            min_node = tmp
            min_node.city_list = tmp.city_list.copy()
            min_node.city_list.append(p)
            min_node.length = whole_length
            up = whole_length #更新上界继续缩小范围
        continue
    for i in range(N):
        if tmp.visited[i]==False:
            citys = tmp.city_list.copy()
            citys.append(i)
            visited = tmp.visited.copy()
            visited[i] = True
            next_node=Node(visited=visited,start=tmp.start,end=i,k=tmp.k+1,
                           length=tmp.length+D[tmp.end][i],lb=0,city_list=citys)
            next_node.lb = get_lb(next_node)
            if next_node.lb <= up:
                index += 1
                pq.put((next_node.lb,index,next_node))

min_node.city_list.append(0)

print('算法运行总时间为：{:.4f}'.format(time.time()-start_time))
print('经过城市的顺序为:',min_node.city_list)
print('经过的总距离为：{:.2f}'.format(min_node.length))

