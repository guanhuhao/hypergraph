from numpy import Inf
import data as Data
import random as rand
from queue import PriorityQueue
import pickle as pkl
import eval
import os,sys
import math as math
import time as time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

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

class Partition_3:
    def __init__(self,p = 10,buffer_size=100,path = "./data/github/vertex_stream.txt") -> None:
        self.p = p              # 分区数量
        self.data_path = path   # 
        self.edges_degree,self.fix_degree,self.number_of_vertexs,self.number_of_edges = self.hypergraph_information(self.data_path)
        self.assigned_node = {}
        self.assigned_edge = {}
        self.buffer_size = buffer_size

        self.res_capacity = [math.ceil(self.number_of_vertexs/p) for i in range(p)]
        self.partition_node = [set() for i in range(self.p)]   # 分区点表
        self.core_edges = [set() for i in range(self.p)]

        print("rec_capacity:"+str(self.res_capacity)) 


    def select_core_set(self,top_k,buffer_edges):
        if len(buffer_edges) == 0 : return -1,None,None
        edge_id,test_degree = min([(i,self.fix_degree[i]) for i in top_k],key = lambda x:x[1])
        # edge_id,test_degree = min([(i,self.edges_degree[i]) for i,j in buffer_edges.items()],key = lambda x:x[1])
        # edge_id,test_degree = min([(i,self.edges_degree[i]) for i in top_k],key = lambda x:x[1])
        print("assign %4d degree:%4d"%(edge_id,test_degree))
        # if self.edges_degree[edge_id]>100:
        #     print("len:",len(top_k),"test:",end="")
        #     print([(i,self.edges_degree[i]) for i in top_k])
        # print("select edge:"+str(edge_id)+" degree:"+str(test_degree))

        core_node = set()
        core_edge = edge_id

        hash_par = set()
        # print(buffer_edges)
        # print(top_k)
        for node in buffer_edges[edge_id]:
            if self.assigned_node.get(node) == None : 
                core_node.add(node)
                continue
            hash_par.add(self.assigned_node[node])


        for par in hash_par:
            if self.res_capacity[par] >= self.edges_degree[edge_id] : 
                return par,core_node,core_edge

        
        rand_ls = []
        for par in range(self.p) : # maybe not used
            if self.res_capacity[par] >= self.edges_degree[edge_id]:
                return par,core_node,core_edge
                rand_ls.append(par)

        if len(rand_ls) != 0 : 
            par = rand.choice(rand_ls)
            return par,core_node,core_edge
        return -1,core_node,core_edge

    def hypergraph_information(self,path): # return dic{edge_id:degree},number of vertexs, number of edges
        num_vertex = 0
        data = Data.vertex_stream(path)
        edge_degree = {}
        fix_degree = {}
        while True:
            id,degree,edges = next(data)
            if id == None : break
            num_vertex += 1
            for i in edges:
                if edge_degree.get(i) == None : 
                    fix_degree[i] = 0
                    edge_degree[i] = 0
                fix_degree[i] +=1
                edge_degree[i] += 1
        # print(edge_degree)
        return edge_degree,fix_degree,num_vertex,len(edge_degree)

    def partition(self):
        begin_time = time.time()
        buffer_size =  self.buffer_size          # 样本图大小
        buffer_nodes = []           # 样本图节点
        buffer_edges = {}           # 样本图边集
        top_k = []

        data = Data.vertex_stream(self.data_path) # load data stream

        read_over = False
        cnt = 0
        cnt_edge = 0
        while read_over != True or len(buffer_nodes) != 0:
            
            while read_over == False and len(buffer_nodes) < buffer_size:
                id,degree,edges = next(data)
                cnt += 1
                if cnt % 100 == 0 : print(cnt)
                a = Node(id,degree,edges)

                distributed = False                 # if has core set edge assgned directly 
                if id == None : 
                    read_over = True
                    break
                for i in range(self.p):
                    set_a = self.core_edges[i]
                    set_b = edges
                    inter = set_a & set_b
                    if inter != set():
                        self.res_capacity[i] -= 1
                        self.partition_node[i] |= set([a])
                        distributed = True
                        for edge in edges:
                            self.edges_degree[edge] -= 1
                            if self.assigned_edge.get(edge) != None:
                                self.res_capacity[self.assigned_edge[edge]] +=1 
                        break
                if distributed == True : continue

                buffer_nodes.append(a)      # add to buffer edge 
                for edge in edges:
                    if buffer_edges.get(edge) == None: buffer_edges[edge] = []
                    buffer_edges[edge].append(a)
            if len(top_k)<800:
                top_k = [(i,self.edges_degree[i]) for i,j in buffer_edges.items()]
                top_k.sort(key = lambda x:x[1])
                top_k = [top_k[i][0] for i in range(min(1000,len(top_k)))]
            par, core_node, core_edge = self.select_core_set(top_k,buffer_edges) # get core set
            
            if par == -1:
                par,capacity = max([(i,self.res_capacity[i]) for i in range(self.p)],key = lambda x:x[1])
                # if par == 0: 
                #     for i in range(self.p):
                #         print("partition:",i," res_capacity:",self.res_capacity[i])
                #     print("partition:",par," capacity:",capacity," degree:",self.edges_degree[core_edge]," after:",self.res_capacity[par]-self.edges_degree[core_edge])


            self.res_capacity[par] -= self.edges_degree[core_edge] # add ghh 

            for node in core_node :
                self.assigned_node[node] = par
                buffer_nodes.remove(node)
                for edge in node.edges:
                    self.edges_degree[edge] -= 1 # edges_degre -1
                    if self.assigned_edge.get(edge) != None:
                        self.res_capacity[self.assigned_edge[edge]] += 1 # edges_degre -1
                    if self.edges_degree[edge] == 0:
                        self.assigned_edge[edge] = par
                        if edge in top_k : top_k.remove(edge)
                        del buffer_edges[edge]
                        cnt_edge += 1
                        if cnt_edge % 1000 == 0: print("solve edge:%d buffer edge:%d"%(cnt_edge,len(buffer_edges)))


            self.core_edges[par] |= set([core_edge])
            self.partition_node[par] |= core_node
            if self.assigned_edge.get(core_edge) == None:
                self.assigned_edge[core_edge] = par
                top_k.remove(core_edge)
                del buffer_edges[core_edge]                

        partition_edge = []
        for part in range(len(self.partition_node)):
            partition_edge.append({})
            for node in self.partition_node[part]:
                for edge in node.edges:
                    partition_edge[part][edge] = 0
        
        for i in range(self.p):
            print("partition %2d: vertex:%5d| edge:%d| core_edge:%5d| res_capacity:%5d| "%(i,len(self.partition_node[i]),len(partition_edge[i]),len(self.core_edges[i]),self.res_capacity[i]))

        end_time = time.time()
        print("runtime:",(end_time-begin_time)*1000,"ms   ",int((end_time-begin_time)/60),"min",int((end_time-begin_time))%60,"s")
        print("\n\n")       


        return self.partition_node,partition_edge



if __name__ == '__main__':                  # test code
    # par = Partition_3(path = "./data/github/vertex_stream.txt",p = 10,buffer_size = 50000)
    par = Partition_3(path = "./data/wiki/vertex_stream.txt",p = 16,buffer_size = 1000)
    # par = Partition_3(path = "./data/wiki/vertex_stream_mini.txt",p = 3,buffer_size = 2)
    partition_node,partition_edge = par.partition()
    eval.Eval(partition_node,partition_edge)

        




