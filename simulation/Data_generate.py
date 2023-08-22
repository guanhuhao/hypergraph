import os
import re
current_path = os.path.dirname(os.path.abspath(__file__))
data_path = current_path+"/../data/"
dataset_list = [
    "wiki_new.txt",         "wiki_new.txt-swap.txt",\
    "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",           "out.github-swap.txt",\
    "out.actor-movie",      "out.actor-movie-swap.txt",\
    "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
    ]

for file in dataset_list:
    # if re.match("(.*)ipynb(.*)",file) != None : continue
    # if os.path.isdir(data_path+file) == True : continue
    # if re.match("(.*)orkut(.*)",file) != None : continue
    # if re.match("(.*)tracker(.*)",file) != None : continue
    # if re.match("(.*)rand(.*)",file) != None : continue
        

    print("solving ",file)
    HyperVertex = {}
    HyperEdge = {}
    with open(data_path+file) as data_file:
        for line in data_file:
            sp = r'[ \t]'
            # print(re.split(sp,line[0:-1])[0:2])
            v_id,e_id = re.split(sp,line[0:-1])[0:2]
            v_id = int(v_id)
            e_id = int(e_id)
            if e_id not in HyperEdge:
                HyperEdge[e_id] = []
            if v_id not in HyperVertex:
                HyperVertex[v_id] = []
            HyperEdge[e_id].append(v_id)
            HyperVertex[v_id].append(e_id)
            
    p = 1
    print("load ok")
    while(p<64):
        p *= 2
        print("generate result p=",p)
        if os.path.exists(current_path + "/test_data/"+str(p)) == False:
            os.mkdir(current_path + "/test_data/"+str(p))
        if os.path.exists(current_path + "/test_data/"+str(p)+"/"+str(file)) == False:
            os.mkdir(current_path + "/test_data/"+str(p)+"/"+str(file))
            
        with open(current_path + "/test_data/"+str(p)+"/"+str(file)+"/vertex_info.txt","w") as outfile:
            for v_id,edges in HyperVertex.items():
                outfile.write(str(v_id))
                for edge in edges:
                    outfile.write(" "+str(edge))
                outfile.write("\n")
            outfile.close()
                
        with open(current_path + "/test_data/"+str(p)+"/"+str(file)+"/edge_info.txt","w") as outfile:
            for e_id,vertexs in HyperEdge.items():
                outfile.write(str(e_id))
                for vertex in vertexs:
                    outfile.write(" "+str(vertex))
                outfile.write("\n")
            outfile.close()
        

        