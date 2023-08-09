from ctypes import sizeof
import os
import re
from math import log

def printInfo(part_vertex,part_edge):
    cal = []
    com = []
    print("vertex:",[(i,len(part_vertex[i])) for i in range(p)]," max:",max([ len(part_vertex[i]) for i in range(p)]), " min:",min([ len(part_vertex[i]) for i in range(p)]))
    print("edge:",[(i,len(part_edge[i])) for i in range(p)]," max:",max([ len(part_edge[i]) for i in range(p)]), " min:",min([ len(part_edge[i]) for i in range(p)]))
    for i in range(p):
        cnt = 0
        for v_id in part_vertex[i]:
            if v_id not in HyperVertex : continue
            # if v_id not in part_vertex[i]: continue
            cnt += len(HyperVertex[v_id])
        cal.append((i,cnt))
    print("cal:",cal," max:",max([i[1] for i in cal]), " min:",min([i[1] for i in cal]))

    for i in range(len(part_edge)):
        tmp = 0
        for e_id in part_edge[i]:
            tmp += cross_edge[e_id] - 1
        com.append((i,tmp))
    print("com:",com," max:",max([i[1] for i in com]), " min:",min([i[1] for i in com]))


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
method_list = ["entropy.txt"]
dataset_list =  [
    "wiki_new.txt"
    ]

# "out.actor-movie","out.actor-movie-swap.txt","out.dbpedia-location",\
#                 "out.dbpedia-location-swap.txt","out.dbpedia-team","out.dbpedia-team-swap.txt","wiki_new.txt"   
for method in method_list:
    outfile = open("partition_analyze_"+method+".txt","w")
    for dataset in dataset_list:
        outfile.write("\ndataset:"+dataset+"\n")
        outfile.write("p, k-1, replication factory, v_max, cal_max, comm_max \n")
        # p = 1
        p = 4
        while p < 64:
            p *= 2
            print("p =",p)
            HyperVertex = {}
            HyperEdge = {}
            Partition = {}
            cross_edge = {}
            comm = {}
            part_edge = [{} for i in range(p)]
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
                    cross_edge[tmp[0]] = 0

            with open(p_path,"r")  as f:
                for line in f:
                    tmp = [int(i) for i in line[0:-1].split(" ")]
                    v_id = tmp[0]
                    p_id = tmp[1]
                    Partition[v_id] = p_id
                    part_vertex[p_id].add(v_id)

            for v_id, edges in HyperVertex.items():
                for e_id in edges:
                    if e_id not in part_edge[Partition[v_id]].keys() : 
                        cross_edge[e_id] += 1
                        part_edge[Partition[v_id]][e_id] = 0
                    part_edge[Partition[v_id]][e_id] += 1    

            for i in range(len(part_edge)):
                tmp =0
                for e_id in part_edge[i].keys():
                    tmp += cross_edge[e_id] - 1
                comm[i] = tmp
            print("input: ",max(comm.values())," ",min(comm.values()))
            rec = 1000000
            while True :
                # print(comm.items())
                lst = sorted(comm.items(),key = lambda x:-x[1])
                max_p = lst[0][0]
                min_p = lst[-1][0]
                if (comm[max_p] - comm[min_p]) / comm[max_p] < 0.1: break
                lst = []
                # for v_id in part_vertex[max_p]:
                #     sum = 0
                #     if v_id not in HyperVertex.keys() : continue
                #     for e_id in HyperVertex[v_id]:
                #         sum += -log(len(HyperEdge[e_id])/1000)/len(HyperVertex[v_id])
                #     lst.append((v_id,sum))

                # print("max_p:",max_p," min_p:",min_p)
                # if rec < (comm[max_p]-comm[min_p]) / comm[max_p] : break
                # rec =  (comm[max_p]-comm[min_p]) / comm[max_p]
                # lst = sorted(lst, key = lambda x:-x[1])
                move_set = []
                # move_set.append(lst[-1][0])
                # lst.pop()
                # rec = 0
                # for p_id in range(p):
                #     if p_id == max_p : continue
                #     for e_id in HyperVertex[move_set[0]]:
                #         if e_id in part_edge[p_id].keys():
                #             sum += -log(len(HyperEdge[e_id])/10000) 
                #     if sum > rec:
                #         rec = sum
                #         min_p = p_id
                flag = 0
                for v_id in part_vertex[max_p]:
                    if flag != 0 : break
                    for p_id in range(max_p,p):
                        if p_id == max_p : continue
                        if v_id not in HyperVertex.keys(): continue
                        flagg = 0
                        for e_id in HyperVertex[v_id]:
                            if e_id not in part_edge[p_id]: 
                                flagg = 1
                                break
                        if flagg == 1: continue
                        flag = 1
                        min_p = p_id
                        move_set.append(v_id)
                        break
                if flag == 0: break
                
                printInfo(part_vertex,part_edge)

                print("max_p:",max_p," min_p:",min_p," v_id:",move_set[0])
                test_cnt = 0
                for v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        if e_id not in part_edge[max_p].keys():
                            print("error! e_id:",e_id," p_id:",max_p)
                    for e_id in HyperVertex[v_id]:
                        part_edge[max_p][e_id] -= 1
                        if part_edge[max_p][e_id] == 0:
                            comm[max_p] -= cross_edge[e_id] - 1
                            test_cnt += cross_edge[e_id] - 1
                            cross_edge[e_id] -= 1
                            part_edge[max_p].pop(e_id)
                            # if e_id in part_edge[max_p].keys() : print("__________________________________________")
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    # if p_id == max_p: print("find error")
                                    comm[p_id] -= 1
                # print("test_cnt:",test_cnt)
                
                for v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        if e_id not in part_edge[min_p].keys():
                            cross_edge[e_id] += 1
                            comm[min_p] += cross_edge[e_id] - 1
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    # if p_id == max_p : print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    comm[p_id] += 1
                            part_edge[min_p][e_id] = 0
                        part_edge[min_p][e_id] += 1
                
                for v_id in move_set:
                    Partition[v_id] = min_p
                    part_vertex[max_p].remove(v_id)
                    part_vertex[min_p].add(v_id)

            while True :
                lst = sorted(comm.items(),key = lambda x:-x[1])
                move_set = []
                max_p = lst[0][0]
                min_p = -1
                for e_id in part_edge[max_p].keys():
                    min_p = -1
                    st = set()
                    dic = {}
                    gain = 0
                    for v_id in HyperEdge[e_id]:
                        # if v_id not in part_vertex[max_p]: continue
                        if Partition[v_id] != max_p : continue
                        st.add(v_id)
                        if v_id not in HyperEdge.keys() : continue
                        for edge in HyperVertex[v_id]:
                            if edge not in dic.keys() : dic[edge] = 0  
                            dic[edge] += 1

                    for ee_id,cnt in dic.items():
                        if cnt == part_edge[max_p][ee_id] : 
                            # print("test1:",2 * cross_edge[ee_id] - 2)
                            gain += 2 * cross_edge[ee_id] - 2
                            dic[ee_id] = 0
                    rec = 0
                    for p_id in range(max_p,p):
                        if p_id == max_p: continue
                        loss = 0
                        for ee_id,cnt in dic.items():
                            if ee_id not in part_edge[p_id]:
                                if cnt == 0 :
                                    loss += 2 * cross_edge[ee_id] - 2
                                else : loss += 2 * cross_edge[ee_id]
                                # print("test2:",2 * cross_edge[ee_id] - 2)

                        if gain - loss > rec :
                        # tmp = [i for i in comm]

                        # if comm[max_p] - gain/2 > comm[p_id] + loss/2 :
                            # print("dict:",dic)
                            rec = gain - loss
                            min_p = p_id
                            break
                    if min_p != -1 : 
                        print("final:",rec," gain:",gain," loss:",loss," num_edge:",len(part_edge[min_p]))
                        for v_id in HyperEdge[e_id] :
                            if Partition[v_id] != max_p : continue
                            move_set.append(v_id)
                        break
                
                    
                if min_p == -1 : break
                
                printInfo(part_vertex,part_edge)

                print("max_p:",max_p," min_p:",min_p," v_id:",move_set[0])
                test_cnt = 0
                for v_id in move_set:
                    # print("v part:",Partition[v_id])
                    for e_id in HyperVertex[v_id]:
                        # print(part_edge[max_p].keys())
                        if e_id not in part_edge[max_p].keys():
                            print("error! e_id:",e_id," p_id:",max_p)
                    for e_id in HyperVertex[v_id]:
                        part_edge[max_p][e_id] -= 1
                        if part_edge[max_p][e_id] == 0:
                            comm[max_p] -= cross_edge[e_id] - 1
                            test_cnt += cross_edge[e_id] - 1
                            cross_edge[e_id] -= 1
                            part_edge[max_p].pop(e_id)
                            # if e_id in part_edge[max_p].keys() : print("__________________________________________")
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    # if p_id == max_p: print("find error")
                                    comm[p_id] -= 1
                # print("test_cnt:",test_cnt)
                
                for v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        if e_id not in part_edge[min_p].keys():
                            cross_edge[e_id] += 1
                            comm[min_p] += cross_edge[e_id] - 1
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    # if p_id == max_p : print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    comm[p_id] += 1
                            part_edge[min_p][e_id] = 0
                        part_edge[min_p][e_id] += 1
                
                for v_id in move_set:
                    Partition[v_id] = min_p
                    part_vertex[max_p].remove(v_id)
                    part_vertex[min_p].add(v_id)

                
                # break
            printInfo(part_vertex,part_edge)
            break
        print("output:",max(comm.values())," ",min(comm.values()))