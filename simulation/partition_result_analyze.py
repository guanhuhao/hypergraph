from ctypes import sizeof
import os
import re

data_path = os.getcwd()+"/test_data/"
# p = 1
method_list = ["basic.txt","anti-basic.txt","entropy.txt","HYPE.txt","MinMax.txt","KaHypar.txt"]
# method_list = ["KaHypar.txt"]
dataset_list = [
    "wiki_new.txt",         "wiki_new.txt-swap.txt",\
    "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",           "out.github-swap.txt",\
    "out.actor-movie",      "out.actor-movie-swap.txt",\
    "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
    ]



# "out.actor-movie","out.actor-movie-swap.txt","out.dbpedia-location",\
#                 "out.dbpedia-location-swap.txt","out.dbpedia-team","out.dbpedia-team-swap.txt","wiki_new.txt"   
for method in method_list:
    outfile = open("partition_analyze_"+method+".txt","w")
    for dataset in dataset_list:
        outfile.write("\ndataset:"+dataset+"\n")
        outfile.write("p, k-1, replication factory, v_max, cal_max, comm_max \n")
        p = 1
        while p < 64:
            p *= 2
            print("p=",p)
            HyperVertex = {}
            HyperEdge = {}
            Partition = {}
            part_edge = [set() for i in range(p)]
            part_vertex = [set() for i in range(p)]
            v_path = data_path + str(p) + "/" + dataset + "/vertex_info.txt"
            e_path = data_path + str(p) + "/" + dataset + "/edge_info.txt"
            p_path = data_path + str(p) + "/" + dataset + "/" + method
            flag = 0
            with open(v_path,"r") as f:
                for line in f:
                    tmp = [int(i) for i in line[0:-1].split(" ")]
                    HyperVertex[tmp[0]] = tmp[1:len(tmp)]
                    # if flag <= 2:
                    #     flag += 1
                    #     print("test:",tmp[0]," ",tmp[1:len(tmp)]," ",tmp)

            with open(e_path,"r") as f:
                for line in f:
                    tmp = [int(i) for i in line[0:-1].split(" ")]
                    HyperEdge[tmp[0]] = tmp[1:len(tmp)]

            with open(p_path,"r")  as f:
                for line in f:
                    tmp = [int(i) for i in line[0:-1].split(" ")]
                    v_id = tmp[0]
                    p_id = tmp[1]
                    Partition[v_id] = p_id
                    part_vertex[p_id].add(v_id)

            for v_id, edges in HyperVertex.items():
                for e_id in edges:
                    part_edge[Partition[v_id]].add(e_id)

            # print(part_edge)
            k_1 = sum([len(part) for part in part_edge]) - len(HyperEdge)
            # k_1 = 0
            replication_fac = 1.0* k_1 / (len(HyperEdge) + len(HyperVertex))
            v_max = max([len(i) for i in part_vertex]) 
            comm_max = 0
            cal_max = 0
            for par in part_vertex:
                cnt = 0
                for v_id in par:
                    if v_id not in HyperVertex : continue
                    cnt += len(HyperVertex[v_id])
                cal_max = max(cal_max,cnt)

            for i in range(len(part_edge)):
                tmp =0
                for e_id in part_edge[i]:
                    cnt = -1
                    for p_id in range(p):
                        if e_id in part_edge[p_id] : cnt += 1 
                    tmp += cnt
                    # k_1 += cnt
                comm_max = max(comm_max,tmp)
            # print("n:",len(HyperVertex),"m:",len(HyperEdge))
            # for i in range(len(part_edge)):
            #     print("i:",i," size:",len(part_edge[i]))
            print("p:",p," k-1 metric:",k_1," replication factory:",replication_fac," v_max:",v_max,\
                " cal_max:",cal_max," comm_max:",comm_max)
            outfile.write(str(p)+","+str(k_1)+","+str(replication_fac)+","+str(v_max)+","+str(cal_max)+","+str(comm_max)+"\n")
outfile.close()
    
        
    
# with open()
# for file in os.listdir(data_path):
#     if re.match("(.*)ipynb(.*)",file) != None : continue
#     if os.path.isdir(data_path+file) == True : continue
#     if re.match("(.*)orkut(.*)",file) != None : continue
#     if re.match("(.*)tracker(.*)",file) != None : continue
#     if re.match("(.*)rand(.*)",file) != None : continue

#     print("solving ",file)

#     p = 1
#     while(p<64):
#         p *= 2
#         out_path = "../simulation/test_data/"+str(p)+"/"+file+"/HYPE.txt"
# #         if os.path.exists(out_path) : continue
