import os
import re
import queue
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)
# data_path = "../data/"
# dataset_list = [
#     "wiki_new.txt",         "wiki_new.txt-swap.txt",\
#     "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
#     "out.github",           "out.github-swap.txt",\
#     "out.actor-movie",      "out.actor-movie-swap.txt",\
#     "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
#     ]
# dataset_list = [
#     "wiki_new.txt",
#     "out.github",  
#     ]

# method_list = ["basic","anti-basic","entropy","MinMax","HYPE","KaHyPar","random"]
# method_list = ["random"]

# dataset = "out.github"
dataset = "out.dbpedia-location"
method = "entropy"
# method = "random"
p = 8
mesh_input =  "../simulation/test_data/"+str(p)+"/"+dataset+"/giraph/"+method+".txt"
id_dir = "../simulation/test_data/"+str(p)+"/"+dataset+"/giraph/id-"+method+".txt"
src = -1
edge = {}
with open(mesh_input,"r") as file:
     for line in file:
        line = [int(re.findall(r'\d+', i)[0]) for i in line[0:-1].split(",")]
        u = line[0]
        if src == -1 : src = u 
        if u not in edge : edge[u] = []
        for i in range(2,len(line),2):
            edge[u].append(line[i]) 

verId = {}
with open(id_dir,"r") as file:
    for line in file:
        old,new = line[0:-1].split(",")
        old = int(old)
        new = int(new)
        verId[old] = new

dis = {}
que = queue.Queue()
que.put(src)
dis[src] = 0
while not que.empty():
    front = que.get()
    for tar in edge[front]:
        if tar%2 == 0 :
            if tar in dis and dis[tar] <= dis[front]+1 : continue 
            dis[tar] = dis[front] + 1
        else :
            if tar in dis and dis[tar] <= dis[front] : continue 
            dis[tar] = dis[front]
        # if front%2 == 0 : dis[tar] = dis[front]
        # if front%2 == 1 and tar%2 == 1: dis[tar] = dis[front]
        # if front%2 == 1 and tar%2 == 0: dis[tar] = dis[front] + 1
        que.put(tar)

with open("check-result3.txt","w") as file:
    ls = [(i,j) for i,j in verId.items()]
    ls.sort()
    for i,j in ls:
        if j not in dis: dis[j] = "inf"
        file.write(str(i)+" "+str(dis[j])+"\n")
        

# entropy
                # Input superstep (ms)=3407
                # Setup (ms)=18
                # Shutdown (ms)=10191
                # Superstep 0 ShortestPathComputation (ms)=333
                # Superstep 1 ShortestPathComputation (ms)=183
                # Superstep 2 ShortestPathComputation (ms)=553
                # Superstep 3 ShortestPathComputation (ms)=199
                # Superstep 4 ShortestPathComputation (ms)=116
                # Total (ms)=15007


# random
                # Initialize (ms)=176
                # Input superstep (ms)=5289
                # Setup (ms)=25
                # Shutdown (ms)=10331
                # Superstep 0 ShortestPathComputation (ms)=513
                # Superstep 1 ShortestPathComputation (ms)=419
                # Superstep 2 ShortestPathComputation (ms)=746
                # Superstep 3 ShortestPathComputation (ms)=247
                # Superstep 4 ShortestPathComputation (ms)=476
                # Total (ms)=18049


# HYPE
                # Initialize (ms)=176
                # Input superstep (ms)=3435
                # Setup (ms)=15
                # Shutdown (ms)=9576
                # Superstep 0 ShortestPathComputation (ms)=371
                # Superstep 1 ShortestPathComputation (ms)=233
                # Superstep 10 ShortestPathComputation (ms)=200
                # Superstep 11 ShortestPathComputation (ms)=170
                # Superstep 12 ShortestPathComputation (ms)=141
                # Superstep 13 ShortestPathComputation (ms)=206
                # Superstep 14 ShortestPathComputation (ms)=123
                # Superstep 15 ShortestPathComputation (ms)=176
                # Superstep 16 ShortestPathComputation (ms)=212
                # Superstep 17 ShortestPathComputation (ms)=205
                # Superstep 18 ShortestPathComputation (ms)=111
                # Superstep 2 ShortestPathComputation (ms)=255
                # Superstep 3 ShortestPathComputation (ms)=629
                # Superstep 4 ShortestPathComputation (ms)=366
                # Superstep 5 ShortestPathComputation (ms)=348
                # Superstep 6 ShortestPathComputation (ms)=482
                # Superstep 7 ShortestPathComputation (ms)=571
                # Superstep 8 ShortestPathComputation (ms)=199
                # Superstep 9 ShortestPathComputation (ms)=326
                # Total (ms)=18359