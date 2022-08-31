from numpy import Inf
import data as Data
import random as rand
from queue import PriorityQueue
import pickle as pkl

class Node:
    def __init__(self,id,degree,edges):
        self.id = id
        self.degree = degree
        self.edges = edges

    def __lt__(self,other):
        return self.id<other.id
    
    def print(self):
        print("id:" + str(self.id))
        print("degree:" + str(self.degree))
        print("edges: "+ str(self.edges))

def hypergraph_information():
    data = Data.vertex_stream()
    edge_degree = {}
    while True:
        id,degree,edges = next(data)
        if id == None : break
        for i in edges:
            if edge_degree.get(i) == None : edge_degree[i] = []
            edge_degree[i].append(id)
    return edge_degree

def cal_cost(node,core_edge,edge_degree):
    node_edges = node.edges
    cost = 0
    for i in node_edges:
        if core_edge.get(i) != None : cost += 1/core_edge[i]
        else : cost -= 1
    return cost

def random_core_set(node_list,core_size,edge_degree):
    k = 1
    edge_dic = {}
    core_edge = {}
    core_node = []

    seed = rand.choice(node_list)
    node_list.remove(seed)
    core_node.append(seed)
    for i in seed.edges : core_edge[i] = edge_degree[i]

    while len(core_node) < core_size :
        topk = PriorityQueue()
        for i in node_list:
            # print(i)
            cost = cal_cost(i,edge_dic,edge_degree)
            # print(cost)
            topk.put((-cost,i))

        for i in range(k):
            pri,node = topk.get()
            core_node.append(node)
            node_list.remove(node)
            # print(core_node)
    return core_node,core_edge






if __name__ == '__main__':                  # test code
    p = 10                  # 分区数量
    cur_p = 0               # 当前生成core set数目
    number_of_nodes = 4135  # 节点总数
    buffer_size = 100       # 样本图大小
    buffer_nodes = []       # 样本图节点
    buffer_edges = {}       # 样本图边集

    edge_degree = {i:len(j)for i,j in hypergraph_information().items()}
    data = Data.vertex_stream()

    partition_node = []
    partition_edge = []

    while len(partition_node) < p :
        while len(buffer_nodes) < buffer_size:
            id,degree,edges = next(data)
            if id == None : break
            a = Node(id,degree,edges)
            # a.print()
            buffer_nodes.append(a)

        core_node, core_edge = random_core_set(buffer_nodes,0.25*buffer_size,edge_degree)
        partition_node.append(core_node)
        partition_edge.append(core_edge)


    while True :
        id,degree,edges = next(data)
        if id == None : break
        par_cost = Inf
        par_id = 0
        for id in range(len(partition_edge)):
            core_edge = partition_edge[id]
            cost = 0
            for i in edges:
                if core_edge.get(i) != None : cost -= 1
                else : cost += edge_degree[i]
            
            if cost < par_cost:
                par_cost = cost
                par_id = id

        partition_node[par_id].append(Node(id,degree,edges))
        for i in edges:
            if partition_edge[par_id].get(i) != None : partition_edge[par_id][i] -= 1
            else : partition_edge[par_id][i] = edge_degree[i]

    with open("./data/partition_result.txt","wb") as f:
        pkl.dump((partition_node,partition_edge),f)

    
    for i in range(len(partition_node)):
        print("partition of vertex"+str(i)+":")
        print(len(partition_node[i]))

    print("\n\n")
    for i in range(len(partition_edge)):
        print("partition of edge"+str(i)+":")
        # print(partition_edge[i])
        sum = 0
        for j in partition_edge[i].values():
            sum += j
        print("sum:"+str(sum))

        




