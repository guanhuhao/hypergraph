import random as rand
def preprocess_raw_data(shuffle = True): # preprocess raw data 
    dic = {}
    edges=[]
    hyper_node = {}
    index = 0
    with open("./data/links.tsv") as f:
        for line in f:
            if(line[0] == '#' or line == "\n") : continue
            a,b = line[0:-1].split('\t')
            if dic.get(a) == None : 
                dic[a] = index
                index += 1
            if dic.get(b) == None : 
                dic[b] = index
                index += 1
            if hyper_node.get(dic[b]) == None :
                hyper_node[dic[b]] = []
            hyper_node[dic[b]].append(dic[a])
            edges.append((dic[a],dic[b]))

    nodes = list(hyper_node.keys())
    if shuffle == True : rand.shuffle(nodes)

    with open("./data/vertex_stream.txt","w") as f:
        f.write("# vertex data stream \n")
        f.write("# number of nodes: 4135    number of edges: 119882     types of edges: 4587\n")
        f.write("# node_id | number of coverd hyper edge| hyper edge id|\n\n")
        for i in nodes:
            line = str(i)+" "+str(len(hyper_node[i]))
            for edge in hyper_node[i]: line += " "+str(edge)
            f.write(line+"\n")

def vertex_stream(path = "./data/vertex_stream.txt"):
    with open(path,'r') as f:
        for line in f:
            if(line[0]=='#' or line=='\n') : continue
            data = [int(i) for i in line[0:-1].split(" ")]
            yield data[0],data[1],data[2:]
    while True :
        yield None,None,None


if __name__ == '__main__':                  # test code
    preprocess_raw_data(shuffle = True)

    # f = vertex_stream()
    # print(next(f))