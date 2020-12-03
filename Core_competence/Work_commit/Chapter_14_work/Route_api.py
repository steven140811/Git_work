import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

# 读取pickle数据
file = open('graph.pkl','rb')
graph = pickle.load(file)

# 找到最小开销节点(从U中)
def find_lowest_cost_node(costs):
    #初始化数据
    lowest_cost = float('inf') # 打擂法，初始最小值为正无穷
    lowest_cost_node = None
    # 遍历所有节点
    for node in costs:
        #如果该节点没有被处理
        if not node in processed:
            # 如果当前节点的开销比已经存在的开销小，那么就更新该节点为开销最小节点
            if costs[node] < lowest_cost:
                lowest_cost = costs[node]
                lowest_cost_node = node
    return lowest_cost_node            

# 找到最短路径
def find_shortest_path():
    node = end
    shortest_path = [end]
    # 最终的根节点为start
    while parents[node] != start:
        # 往前移动一步
        node = parents[node]
        # 添加到路径中
        shortest_path.append(node)
    shortest_path.append(start)
        
    return shortest_path

# 计算图中从start到end的最短路径
def dijkstra():
    # 查询到目前开销最小节点
    node = find_lowest_cost_node(costs)
    # print('当前cost最小节点：',node)
    # 使用找到的开销最小的节点，计算它的令居，是否可以通过它进行更新
    # 如果所有的节点都在processed里面，就结束
    while node is not None:
        # 获取节点的cost
        cost = costs[node] # cost是从node到start
        # 获取节点的邻居
        neighbors = graph[node]
        # 遍历所有邻居，看是否可以通过它进行更新
        for neighbor in neighbors.keys():
            # 计算邻居到当前节点 + 当前节点开销
            new_cost = cost + float(neighbors[neighbor])
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                # 经过node到达neighbor节点，cost更少
                parents[neighbor] = node
        # 将当前节点标记为已处理
        processed.append(node)
        # 下一步，继续找U中最短距离的节点 costs=U,processed=S
        node = find_lowest_cost_node(costs)
        # print('当前cost最小节点：',node)
    
    # 循环完，说明所有节点已经处理完
    shortest_path = find_shortest_path()
    shortest_path.reverse()
    # print('从{}到{}的最短路径：{}'.format(start,end,shortest_path))
    return shortest_path
    
def compute(site1,site2):
    global start,end,costs,parents,processed
    
    start = site1
    end = site2
    
    # 创建节点的开销表，cost是指从start到该节点的距离
    costs = {}
    # 存储父节点的Hash表，用于记录路径
    parents = {} 
    parents[end] = None

    # 获取节点相邻的节点
    #print(graph[start].keys())  dict_keys(['知春路站', '上地站'])
    for node in graph[start].keys():
        costs[node] = float(graph[start][node])
        parents[node] = start
    #终点到起始点设置为无穷大
    costs[end] = float('inf')

    # 记录处理过的节点list
    processed = []

    shortest_path = dijkstra()
    return shortest_path

if __name__ == '__main__':
    shortest_path = Route_api.compute(site1,site2)
    print(shortest_path)