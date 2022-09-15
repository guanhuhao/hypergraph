from numpy import Inf
import data as Data
import random as rand
from queue import PriorityQueue
import pickle as pkl
import eval
import os,sys
import math as math
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

class Partition_1:
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



    def partition_1():
        p = 10                  # 分区数量
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

class Partition_2:
    @classmethod
    def select_core_set(self,buffer_nodes,buffer_edges,coreset_size):
        edge_id = min([(i,len(j)) for i,j in buffer_edges.items()],key = lambda x:x[1])[0]
        # ls.sort(key = lambda x : -x[1])
        print(edge_id)

        core_node = set()
        core_edge = set()
        # print(len(core_node))

        # print(ls[-1][1])
        core_edge.add(edge_id)
        for node in buffer_edges[edge_id]:
            core_node.add(node)

        # for node in core_node:
        #     for edge in node.edges:
        #         buffer_edges[edge].remove(node)

        for edge in [i for i in core_edge]:
            del buffer_edges[edge]

        return core_node,core_edge

    @classmethod
    def partition_2(self):
        p = 10                  # 分区数量
        data_size = 4125
        max_capacity = 1000
        buffer_size = 2000       # 样本图大小
        buffer_nodes = []       # 样本图节点
        buffer_edges = {}       # 样本图边集

        data = Data.vertex_stream("./data/github/vertex_stream.txt") # load data stream
        # data = Data.vertex_stream("./data/vertex_stream.txt")
        partition_node = [[] for i in range(p)]
        partition_edge = [[] for i in range(p)]

        read_over = False
        while read_over == False :
            
            while len(buffer_nodes) < buffer_size:
                id,degree,edges = next(data)
                a = Node(id,degree,edges)

                distributed = False                 # core_set distribution 
                if id == None : 
                    read_over = True
                    break
                for i in range(len(partition_edge)):
                    set_a = set(partition_edge[i])
                    set_b = set(edges)
                    if set_a & set_b != set():
                        partition_node[i] += [a]
                        distributed = True
                        break
                if distributed == True : continue

                buffer_nodes.append(a)
                for edge in edges:
                    if buffer_edges.get(edge) == None: buffer_edges[edge] = []
                    buffer_edges[edge].append(a)

            core_node, core_edge = self.select_core_set(buffer_nodes,buffer_edges,buffer_size*0.25)
            # core_node, core_edge = self.select_core_set(buffer_nodes,buffer_edges,2)
            
            # print(buffer_nodes)
            # print(core_node)

            min_id = 0
            for i in range(0,len(partition_node)):
                if len(partition_node[i]) < len(partition_node[min_id]) : min_id = i

            # print()
            
            if len(partition_node[min_id]) > 200 : 
                break

            print("min_id:"+str(min_id)+" add node:"+str(len(core_node)))
            partition_node[min_id] += core_node
            partition_edge[min_id] += core_edge
            # for edge in core_edge : del buffer_edges[edge] 

            print("core set:" +str(core_node))
            for node in core_node:
                print("del node:"+str(node))
                buffer_nodes.remove(node)

        for i in range(len(partition_edge)):
            print("part "+str(i) +" lenth:" +str(len(partition_edge[i])))
        
        while True:
            id,degree,edges = next(data)
            if id == None : break
            par_cost = Inf
            par_id = 0
            for id in range(len(partition_edge)):
                core_edge = partition_edge[id]
                cost = 0
                for i in edges:
                    if i in core_edge : cost -= 1
                
                if cost < par_cost:
                    par_cost = cost
                    par_id = id
            # print(par_id)

            partition_node[par_id].append(Node(id,degree,edges))

        partition_edge = []
        for part in range(len(partition_node)):
            partition_edge.append({})
            for node in partition_node[part]:
                for edge in node.edges:
                    partition_edge[part][edge] = 0


        with open("./data/partition_result.txt","wb") as f:
            pkl.dump((partition_node,partition_edge),f)

        
        for i in range(len(partition_node)):
            print("partition of vertex"+str(i)+":"+str(len(partition_node[i])))
            # print(len(partition_node[i]))

        print("\n\n")

        return partition_node,partition_edge
        # for i in range(len(partition_edge)):
        #     print("partition of edge"+str(i)+":")
        #     # print(partition_edge[i])
        #     sum = 0
        #     for j in partition_edge[i].values():
        #         sum += j
        #     print("sum:"+str(sum))


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


    def select_core_set(self,buffer_nodes,buffer_edges):
        if len(buffer_edges) == 0 : return -1,None,None
        # edge_id,test_degree = min([(i,self.fix_degree[i]) for i,j in buffer_edges.items()],key = lambda x:x[1])
        edge_id,test_degree = min([(i,self.edges_degree[i]) for i,j in buffer_edges.items()],key = lambda x:x[1])
        # print("select edge:"+str(edge_id)+" degree:"+str(test_degree))

        core_node = set()
        core_edge = edge_id

        hash_par = set()
        for node in buffer_edges[edge_id]:
            if self.assigned_node.get(node) == None : 
                core_node.add(node)
                continue
            hash_par.add(self.assigned_node[node])


        for par in hash_par:
            if self.res_capacity[par] >= self.edges_degree[edge_id] : 
                return par,core_node,core_edge

        for par in range(self.p) : # maybe not used
            if self.res_capacity[par] >= self.edges_degree[edge_id]:
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
        buffer_size =  self.buffer_size          # 样本图大小
        buffer_nodes = []           # 样本图节点
        buffer_edges = {}           # 样本图边集

        data = Data.vertex_stream(self.data_path) # load data stream

        read_over = False
        cnt = 0
        cnt_free = 0
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
                # if id == 1575: print("buffer add node:"+str(id))
                for i in range(self.p):
                    set_a = self.core_edges[i]
                    set_b = edges
                    inter = set_a & set_b
                    # print("set_a:"+str(set_a)+" set_b:"+str(set_b)+" inter:"+str(inter))
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
                # print("node pass:"+str(id))

                buffer_nodes.append(a)      # add to buffer edge 
                for edge in edges:
                    if buffer_edges.get(edge) == None: buffer_edges[edge] = []
                    buffer_edges[edge].append(a)
            # print("test:"+str(self.edges_degree[900]))
            par, core_node, core_edge = self.select_core_set(buffer_nodes,buffer_edges) # get core set
            cnt_edge += 1
            if cnt_edge % 1000 == 0: print("solve edge:%d buffer edge:%d"%(cnt_edge,len(buffer_edges)))
            
            if par == -1:
                par,capacity = max([(i,self.res_capacity[i]) for i in range(self.p)],key = lambda x:x[1])
            
            # if len(core_node) != 0 :
            #     print("add node:",end="")
            #     for i in core_node:
            #         print(i.id,end=" ")
            #     print()
            # print("edge_id:"+str(core_edge)+" degree:"+str(self.edges_degree[core_edge])+" add partition:"+str(par)+" res_capacity:"+str(self.res_capacity[par])+" cur_capcity:"+str(len(self.partition_node[par]))) 

            if  len(buffer_edges) == 0  :
                # print(123)
                remove_list = []
                for node in buffer_nodes:
                    edges = node.edges
                    for par in range(self.p):
                        if (self.core_edges[par] & edges) != set():
                            remove_list.append((node,par))
                            self.res_capacity[par] -= 1
                print("remove:"+str(len(remove_list)))
                # print(len(buffer_edges))
                # print(len(buffer_nodes))
                # print("rec_capacity:"+str(self.res_capacity))
                # print("core_edge"+str(self.core_edges))

                        
                # if len(remove_list) == 0:
                #     free_size = min(len(buffer_nodes),math.ceil(0.1 * buffer_size))
                #     # print(123)
                #     # free_size =math.min(10)
                #     cnt_free += free_size
                #     for i in range(int(free_size)):
                #         id,value = max([(i,self.res_capacity[i]) for i in range(self.p)],key = lambda x:x[1])
                #         self.res_capacity[id] -= 1
                #         remove_list.append((buffer_nodes[i],id))

                    # for node,id in remove_list:
                    #     print("random remmove:%d partition:%d"%(node.id,id))

                    
                    # for 
                for node,par in remove_list:
                    # print("remove:"+str(node.id))
                    self.partition_node[par].add(node)
                    self.assigned_node[node] = par
                    for edge in node.edges:
                        self.edges_degree[edge] -= 1 # edges_degre -1
                        if self.assigned_edge.get(edge) != None:
                            self.res_capacity[self.assigned_edge[edge]] += 1 # edges_degre -1
                    buffer_nodes.remove(node)
                if core_edge != None : del buffer_edges[core_edge]

            else :
                # print("degree:"+str(self.edges_degree[core_edge]))
                self.res_capacity[par] -= self.edges_degree[core_edge] # add ghh 

                for node in core_node :
                    self.assigned_node[node] = par
                    buffer_nodes.remove(node)
                    for edge in node.edges:
                        self.edges_degree[edge] -= 1 # edges_degre -1
                        if self.assigned_edge.get(edge) != None:
                            self.res_capacity[self.assigned_edge[edge]] += 1 # edges_degre -1

                self.core_edges[par] |= set([core_edge])
                self.assigned_edge[core_edge] = par
                self.partition_node[par] |= core_node
                # self.res_capacity[par] -= self.edges_degree[core_edge]
                del buffer_edges[core_edge]
            # if len(core_node) != 0 :
            #     print("add node:"," ")
            #     for i in core_node:
            #         print(i.id," ")

                

        partition_edge = []
        for part in range(len(self.partition_node)):
            partition_edge.append({})
            for node in self.partition_node[part]:
                for edge in node.edges:
                    partition_edge[part][edge] = 0


        # with open("./data/partition_result.txt","wb") as f:
        #     pkl.dump((partition_node,partition_edge),f)

        
        for i in range(self.p):
            # print("partition "+str(i)+": vertex:"+str(len(self.partition_node[i]))+"  edge:" +str(len(self.core_edges[i]))+" res_capacity:"+str(self.res_capacity[i]))
            print("partition %2d: vertex:%5d| edge:%d| core_edge:%5d| res_capacity:%5d| "%(i,len(self.partition_node[i]),len(partition_edge[i]),len(self.core_edges[i]),self.res_capacity[i]))

            # print(len(partition_node[i]))
        print("free_size:%d"%cnt_free)
        print("\n\n")

        # for node,par in self.assigned_node.items():
        #     if self.assigned_node[node] != 0:
        #         for edge in node.edges:
        #             if self.assigned_edge.get(edge) == None : continue
        #             if self.assigned_edge[edge] == 0:
        #                 print("node:%d assigned:%d"%(node.id,self.assigned_node[node]))


        return self.partition_node,partition_edge



if __name__ == '__main__':                  # test code
    par = Partition_3(path = "./data/github/vertex_stream.txt",p = 10,buffer_size = 2000)
    # par = Partition_3(path = "./data/wiki/vertex_stream.txt",p = 10,buffer_size = 4100)
    # par = Partition_3(path = "./data/wiki/vertex_stream_mini.txt",p = 3,buffer_size = 2)
    partition_node,partition_edge = par.partition()
    eval.Eval(partition_node,partition_edge)

        




