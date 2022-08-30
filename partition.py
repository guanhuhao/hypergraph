import data as Data
import random as rand

class Node:
    def __init__(self,id,degree,edges):
        self.id = id
        self.degree = degree
        self.edges = edges
    
    def print(self):
        print("id:" + str(self.id))
        print("degree:" + str(self.degree))
        print("edges: "+ str(self.edges))

def hyper_edge_information():
    data = Data.vertex_stream()
    dic = {}
    while True:
        id,degree,edges = next(data)
        if id == None : break
        for i in edges:
            if dic.get(i) == None : dic[i] = 0
            dic[i] += 1
    return dic 

def random_core_set(node_list,core_size):
    edge_dic = {}

    core_set = []
    seed = rand.choice(node_list)
    core_set.append(seed)
    while core_set < core_size :
        for i in node_list:



if __name__ == '__main__':                  # test code
    p = 10                  # 分区数量
    cur_p = 0               # 当前生成core set数目
    number_of_nodes = 4135  # 节点总数
    buffer_size = 10        # 样本图大小
    buffer_nodes = []       # 样本图节点
    buffer_edges = {}       # 样本图边集


    data = Data.vertex_stream()

    while cur_p < p :
        while len(buffer_nodes) < buffer_size:
            id,degree,edges = next(data)
            a = Node(id,degree,edges)
            a.print()
            buffer_nodes.append(a)



    print(hyper_edge_information())

