import os
import re
import math
import time 
import pytz
import datetime

current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)
data_path = "../../data/"
dataset_list = [
    # "wiki_new.txt",         "wiki_new.txt-swap.txt",\
    # "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",       #     "out.github-swap.txt",\
    # "out.actor-movie",      "out.actor-movie-swap.txt",\
    # "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
    "out.dblp-author",  # "out.dblp-author-swap.txt",\
    # "out.orkut-groupmemberships",  "out.orkut-groupmemberships-swap.txt",\
    # "out.trackers",         "out.trackers-swap.txt",\
    ]
# dataset_list = [
#     "wiki_new.txt",
#     "out.github",  
#     ]

# method_list = ["basic","anti-basic","entropy","MinMax","HYPE","KaHyPar","random","NoPar"]
method_list = ["entropy","KaHyPar","HYPE","random"]
# method_list = ["MinMax","HYPE","random","NoPar"]
# method_list = ["anti-basic","entropy"]
# method_list = ["NoPar"]

for dataset in dataset_list:
    # p = 1
    Edge = {}
    EdgeInfoPath = "/back-up/large-cluster/comm/test_data/2/"+dataset+"/edge_info.txt"
    with open(EdgeInfoPath) as file:   # e_id, v1_id, v2_id,...
        for line in file:
            data = line[0:-1].split(" ")
            e_id = int(data[0])
            Edge[e_id] = [int(i) for i in data[1:]]
            
    for method in method_list:
        p = 16
        while p < 32:
            timestamp = datetime.datetime.now()
            desired_timezone = pytz.timezone('Asia/Shanghai')
            localized_time = desired_timezone.localize(timestamp)
            formatted_time = localized_time.strftime("%Y-%m-%d %H:%M:%S\t")
          
            print(formatted_time)

            if method != "NoPar" :
                p *= 2
            vertex_partition = "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/"+method+".txt"



                    
            # vertex_info =  "../../simulation/test_data/"+str(p)+"/"+dataset+"/flink/"+method+"-vertex.txt"
            edge_info =  "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/powergraph/"+method+"-edge.txt"

            # id_dir = "../../simulation/test_data/"+str(p)+"/"+dataset+"/flink/id-"+method+".txt"
            directory = os.path.dirname(edge_info)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if os.path.exists(edge_info) : 
                print("p:",p," dataset:",dataset," method:",method," already ok")
                continue

            # print("path:",vertex_partition)
            # print("dataset:",dataset)
            print("solving dataset:",dataset," method:",method," p:",p)

            lst = []
            n2p = {} # nid -> pid 
            e2p = {} # eid -> [pid1,pid2,...]
            e2n = {} # (eid,pid) -> nid
            shift = 0
            with open(vertex_partition,"r") as file:
                for line in file:
                    n_id,p_id = re.split(r'\s+', line[0:-1])
                    n_id = int(n_id)
                    p_id = int(p_id)
                    n2p[n_id] = p_id
                    shift = max(n_id+1,shift)

            delta = 0
            edgeList = {}
            for eid,nodes in Edge.items():
                for nid in nodes:
                    pid = n2p[nid] 
                    if (pid,eid) not in e2n:
                        if eid not in e2p : e2p[eid] = []
                        e2p[eid].append(pid) 
                        e2n[(pid,eid)] = shift + delta
                        n2p[shift + delta] = pid
                        delta += 1
                    u = nid
                    v = e2n[(pid,eid)]
                    if u not in edgeList : edgeList[u] = []
                    if v not in edgeList : edgeList[v] = []
                    edgeList[u].append(v)
                    edgeList[v].append(u)

            for eid,parts in e2p.items():
                check = {}
                for pid1 in parts:
                    for pid2 in parts:
                        if pid1 == pid2 : continue
                        if (pid1,pid2) in check or (pid2,pid1) in check : continue 
                        if u not in edgeList : edgeList[u] = []
                        if v not in edgeList : edgeList[v] = []

                        u = e2n[(pid1,eid)]
                        v = e2n[(pid2,eid)]
                        edgeList[u].append(v)
                        edgeList[v].append(u)
                        check[(u,v)] = 1
                        check[(v,u)] = 1

            # with open(vertex_info,'w') as files:
            #     ls = list(edgeList.items())
            #     ls.sort()
            #     for nid,edges in ls:
            #         u = (nid*p+n2p[nid])*2 + min(int(nid/shift),1)
            #         line = str(u)+","+"0\n"
            #         files.write(line)

            with open(edge_info,'w') as files:
                ls = list(edgeList.items())
                ls.sort()
                for nid,edges in ls:
                    u = (nid*p+n2p[nid])*2 + min(int(nid/shift),1)
                    # line = str(u)+","+""
                    for eid in edges:
                        v = (eid*p+n2p[eid])*2 + min(int(eid/shift),1)
                        files.write(str(u) + " " + str(v) + " " + str(n2p[nid]) + "\n")
                        # line += "[" + str(v) + "," + str(1) +"],"
            print("vertex Num:",len(edgeList)," Edge Num:",sum([len(i) for i in edgeList.values()]))

            if method == "NoPar" :
                break

            # with open(id_dir,'w') as files:
            #     ls = [(nid,edges) for nid,edges in edgeList.items()]
            #     ls.sort()
            #     for nid,edges in ls:
            #         u = (nid*p+n2p[nid])*2 + min(int(nid/shift),1)
            #         files.write(str(nid)+","+str(u)+"\n")

            # with open(check_file,"w") as files: 
            #     for key,val in dic.items():
            #         files.write(str(val)+" "+str(key)+"\n")

            # with open()
            # break