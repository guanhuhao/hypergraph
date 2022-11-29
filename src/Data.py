import heapq
import matplotlib.pyplot as plt # 画曲线图
import numpy as np #拟合直线

class HyperNode:
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

class HyperEdge:
    def __init__(self,id,degree,nodes):
        self.id = id
        self.degree = degree 
        self.nodes = nodes
        
    def print(self):
        print("id:" + str(self.id))
        print("degree:" + str(self.degree))
        print("edges: "+ str(self.nodes))


class Heap:
    def __init__(self):
        self.heap = []
        self.check = set()
        
    def add(self,rank,item):
        if item in self.check : return
        heapq.heappush(self.heap,(rank,item))
        self.check.add(item)
        
    def pop(self):
        rank,item = heapq.heappop(self.heap)
        self.check.remove(item)
        return rank,item
    
    def clear(self):
        self.check.clear()
        self.heap = []
        
    def check(self,item):
        return item in self.check
    
    def size(self):
#         print(self.heap)
        return len(self.heap)
    
    def top(self):
        return self.heap[0]
    
    def remake(self,ls):
#         print("before:",self.heap)
        heapq.heapify(ls)
        self.heap = ls
#         print("after:",self.heap)


class K_core:
    def __init__(self,path):
        self.path = path
        self.node,self.edge = load_data(path)
#         print(self.node)
    def get_kcore(self,mini_size):
        mp_node = {key:value.degree for key,value in self.node.items()}
        mp_edge = {key:value.degree for key,value in self.edge.items()}
        k = 0
        while len(mp_node) > 0:
            del_node = []
            del_edge = []
            for node_id,degree in mp_node.items():
                if degree <= k : del_node.append(node_id)
            for edge_id,degree in mp_edge.items():
                if degree <= k : del_edge.append(edge_id)
            if len(mp_node) - len(del_node) < mini_size : 
                return [self.node[node_id] for node_id in mp_node.keys()]
            for node_id in del_node:
                for edge_id in self.node[node_id].edges:
                    if edge_id not in mp_edge.keys() : continue
                    mp_edge[edge_id] -= 1
                del mp_node[node_id]
            for edge_id in del_edge:
                for node_id in self.edge[edge_id].nodes:
                    if node_id not in mp_node.keys() : continue
                    mp_node[node_id] -= 1
                del mp_edge[edge_id]
            k += 1
        
            
    def del_node(self,nodes):
        for node in nodes:
            if node.id not in self.node.keys() : continue
            for edge_id in node.edges:
                if edge_id not in self.edge.keys() : continue
                self.edge[edge_id].degree -= 1
                if self.edge[edge_id].degree == 0 :
                    del self.edge[edge_id]
            del self.node[node.id]
            
    def find_connection(self,nodes):
        ret  = set()
        ret.add(nodes[0])
        for edge_id in nodes[0].edges:
            for node in nodes[1:-1]:
                if node.id in self.edge[edge_id].nodes: 
                    ret.add(node)
        return ret
            

# return: mp_node,mp_edge
def load_data(path):
    # input:
    # path: data set path
    
    # return: 
    # mp_node: dict of partition node n_id:HyperNode
    # mp_edge: dict of partition edge e_id:HyperEdge
    
    mp_node = {}
    mp_edge = {}
    with open(path,'r') as f:
        for line in f:
#             print(line[0:-1].split(" "))
            n_id,e_id = line[0:-1].split(" ")
            if mp_node.get(n_id) == None : 
                mp_node[n_id] = HyperNode(n_id,0,set())
            if mp_edge.get(e_id) == None :
                mp_edge[e_id] = HyperEdge(e_id,0,set())
                
            mp_node[n_id].degree += 1
            mp_edge[e_id].degree += 1
            mp_node[n_id].edges.add(e_id)
            mp_edge[e_id].nodes.add(n_id)
    return mp_node,mp_edge    


# return: None
def recoder(part_node,mp_node,mp_edge,path):
    # input:
    # part_node: result of partition nodemp_eval[node.id] - node.degree
    # mp_node: dictionary of hyper node 
    # mp_edge: dictionary of hyper edge
    # path: path to save record result
    
    dic = {}
    tot = 0
    for par in part_node:
        for node in par:
            dic[node.id] = len(dic)

    print(path+"/record.txt")
    with open(path+"/record.txt",'w') as f:
        for par in part_node:
            for node in par:
                for edge in node.edges:
                    f.write(str(dic[node.id])+" "+str(edge)+"\n")

            

def degree_distribute(mp_node,show = True,logx=True,logy=True,coeff = True,cumulation = True): # draw degree distribute graph 
    degree = mp_node
    dic = {j.degree:0 for i,j in degree.items()}
    
    for i,j in degree.items(): dic[j.degree] += 1
    
    ls = sorted(dic.items(), key = lambda x:(x[0],x[1]))
        
    x = [i[0] for i in ls]
    y = [i[1] for i in ls]

    if x[0] == 0:
        x = x[1:-1]
        y = y[1:-1]
    
    if cumulation == True : 
        cnt = sum(y)
        for i in range(len(x)):
            cnt -= y[i]
            y[i] += cnt

    if show == True :
        plt.plot(x,y, 'o',color='b')
        if logy : plt.yscale('log')
        if logx : plt.xscale('log')
        

    if coeff == True : 

        xx = [np.log2(i) for i in x]
        yy = [np.log2(i) for i in y]
        
        k,b = np.polyfit(xx, yy, 1)
#         lg = yy[0]/xx[-1]
#         lg = 1/lg
        print("alpha: "+str(k))
        
        xx = x
        yy = [(i**k)*(2**b) for i in xx]
        plt.plot(xx,yy,color='r')
    plt.show()

    return [(x[i],y[i]) for i in range(len(x))]