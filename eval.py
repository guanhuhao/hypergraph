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

def Eval(partition_node,partition_edge):
    dic = {}
    for par in partition_edge:
        for edge in par:
            if dic.get(edge) == None : dic[edge] = 0
            dic[edge] += 1
    print("total hyperedge: "+str(len(dic)))
    print("k-1: " + str(sum(dic.values())-len(dic)))

    no_cross = 0
    for i in dic.values(): 
        if i == 1 : no_cross += 1
    print("hyperedge without cross:" +str(no_cross))

if __name__ == '__main__':
    # dic = {1:0}
    # for i,j in dic.items():
    #     print(i)
    #     print(j)
    with open('./data/partition_result.txt',"rb") as f:
        partition_node,partition_edge = pkl.load(f)
        Eval(partition_node,partition_edge)
        