import os
import re
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)
data_path = "../data/"
dataset_list = [
    "wiki_new.txt",         "wiki_new.txt-swap.txt",\
    "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",           "out.github-swap.txt",\
    "out.actor-movie",      "out.actor-movie-swap.txt",\
    "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
    ]
# dataset_list = [
#     "wiki_new.txt"
#     ]

method_list = ["basic","anti-basic","entropy","MinMax","HYPE","KaHyPar","random"]
# method_list = ["random"]

for dataset in dataset_list:
    for method in method_list:
        p = 1
        Edge = {}
        EdgeInfoPath = "../simulation/test_data/2/"+dataset+"/edge_info.txt"
        with open(EdgeInfoPath) as file:   # e_id, v1_id, v2_id,...
            for line in file:
                data = line[0:-1].split(" ")
                e_id = int(data[0])
                Edge[e_id] = [int(i) for i in data[1:]]
        # print(Edge)

        while p < 64:
            p *= 2
            vertex_partition = "../simulation/test_data/"+str(p)+"/"+dataset+"/"+method+".txt"
            # print("path:",vertex_partition)
            # print("dataset:",dataset)
            print("solving dataset:",dataset," method:",method," p:",p)
            edgeInfo= "../simulation/test_data/"+str(p)+"/"+dataset+"/HYPE.txt"
            lst = []
            dic = {}
            with open(vertex_partition,"r") as file:
                for line in file:
                    n_id,p_id = re.split(r'\s+', line[0:-1])
                    n_id = int(n_id)
                    p_id = int(p_id)
                    lst.append((p_id,n_id))
                    # print(n_id," ",p_id)
                    # break
                sorted(lst)
                cnt = 0

                for p_id,n_id in lst:
                    cnt += 1
                    dic[n_id] = cnt
            
            mesh_input =  "../simulation/test_data/"+str(p)+"/"+dataset+"/mesh_input/mesh-"+method+".txt"
            check_file =  "../simulation/test_data/"+str(p)+"/"+dataset+"/mesh_input/check-mesh-"+method+".txt"
            directory = os.path.dirname(mesh_input)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(mesh_input,'w') as files:
                for e_id,nodes in Edge.items():
                    for n_id in nodes:
                        files.write(str(e_id)+","+str(dic[n_id])+"\n")

            with open(check_file,"w") as files: 
                for key,val in dic.items():
                    files.write(str(val)+" "+str(key)+"\n")

            # with open()
            # break