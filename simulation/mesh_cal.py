import os
import re
import math
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
dataset_list = [
    "out.github",   
    ]

method_list = ["basic", "anti-basic", "entropy", "MinMax", "HYPE", "KaHyPar", "random"]
method_list = ["entropy", "HYPE", "random"]


for dataset in dataset_list:
    for method in method_list:
        p = 16
        st = []
        for i in range(p) : 
            st.append(set())

        mesh_input =  "../simulation/test_data/"+str(p)+"/"+dataset+"/mesh_input/mesh-"+method+".txt"
        # check_file =  "../simulation/test_data/"+str(p)+"/"+dataset+"/mesh_input/check-mesh-"+method+".txt"
        directory = os.path.dirname(mesh_input)
        if not os.path.exists(directory):
            os.makedirs(directory)
        edges = []
        n_max = 0
        e_max = 0
        with open(mesh_input,'r') as files:
            for line in files:
                e_id,n_id = line[:-1].split(",")
                e_id = int(e_id)
                n_id = int(n_id)
                edges.append((e_id,n_id))
                n_max = max(n_max,n_id)
                e_max = max(e_max,e_id)
            capcity = math.ceil(n_max/p)
            for e_id,n_id in edges:
                pp = math.floor(n_id/capcity)
                st[pp].add(e_id)

            print("dataset:",dataset," method:",method," k-1:",sum([len(i) for i in st])-e_max)


            # for e_id,nodes in Edge.items():
            #     for n_id in nodes:
            #         files.write(str(e_id)+","+str(dic[n_id])+"\n")
