from ctypes import sizeof
import os
import re
from math import log
import time
def printInfo(part_vertex,part_edge):
    cal = []
    com = []
    tmp = [(i,len(part_vertex[i])) for i in range(p)]
    print("vertex:",tmp," max:",max([ j for i,j in tmp ]), " min:",min([j for i,j in tmp])," sum:",sum([j for i,j in tmp]))
    tmp = [(i,len(part_edge[i])) for i in range(p)]
    print("edge:",tmp," max:",max([ j for i,j in tmp ]), " min:",min([j for i,j in tmp])," sum:",sum([j for i,j in tmp]))

    for i in range(p):
        cnt = 0
        for v_id in part_vertex[i]:
            if v_id not in HyperVertex : continue
            # if v_id not in part_vertex[i]: continue
            cnt += len(HyperVertex[v_id])
        cal.append((i,cnt))
    print("cal:",cal," max:",max([i[1] for i in cal]), " min:",min([i[1] for i in cal])," sum:",sum([i[1] for i in cal]))

    for i in range(len(part_edge)):
        tmp = 0
        for e_id in part_edge[i]:
            tmp += cross_edge[e_id] - 1
        com.append((i,tmp))
    print("com:",com," max:",max([i[1] for i in com]), " min:",min([i[1] for i in com])," sum:",sum([i[1] for i in  com]))

def check(part_edge,cross_edge):
        check_part_edge = [{} for i in range(p)]  # check part_edge
        for v_id, edges in HyperVertex.items():
            for e_id in edges:
                if e_id not in check_part_edge[Partition[v_id]].keys() : 
                    check_part_edge[Partition[v_id]][e_id] = 0
                check_part_edge[Partition[v_id]][e_id] += 1  

        for p_id in range(p):
            for e_id,value in part_edge[p_id].items():
                if part_edge[p_id][e_id] != check_part_edge[p_id][e_id]:
                    print("error! e_id:",e_id," A:",part_edge[p_id][e_id]," B:",check_part_edge[p_id][e_id])

        check_cross_edge = {}
        for e_id,nodes in HyperEdge.items():
            st = set()
            check_cross_edge[e_id] = 0
            for v_id in nodes:
                if Partition[v_id] not in st:
                    st.add(Partition[v_id])
                    check_cross_edge[e_id] += 1


        for e_id,val in cross_edge.items():
            if val != check_cross_edge[e_id]:
                print("e_id:",e_id," fact:",check_cross_edge[e_id]," predict:",val)
                print("cross_edge error!")
                break




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
    #  "out.dbpedia-location"
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
            cal = {}
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

            for i in range(p):
                cnt = 0
                for v_id in part_vertex[i]:
                    if v_id not in HyperVertex : continue
                    cnt += len(HyperVertex[v_id])
                cal[i] = cnt
            # print("cal:",cal," max:",max([i[1] for i in cal]), " min:",min([i[1] for i in cal]))


            beg_time = time.time()
            while True :
                for i in range(p):
                    cnt = 0
                    for v_id in part_vertex[i]:
                        if v_id not in HyperVertex : continue
                        cnt += len(HyperVertex[v_id])
                    cal[i] = cnt
                # print("cal:",cal," max:",max([i[1] for i in cal]), " min:",min([i[1] for i in cal]))

                lst = sorted(cal.items(),key = lambda x:-x[1])
                max_p = lst[0][0]
                move_set = []
                delta = [0 for i in range(p)]

                for v_id in part_vertex[max_p]:
                    for p_id in range(max_p,p):
                        if p_id == max_p : continue
                        if v_id not in HyperVertex.keys(): continue
                        if cal[max_p] + delta[max_p] - len(HyperVertex[v_id]) < cal[p_id] + delta[p_id] +  len(HyperVertex[v_id]) : continue
                        flagg = 0
                        for e_id in HyperVertex[v_id]:
                            if e_id not in part_edge[p_id]: 
                                flagg = 1
                                break
                        if flagg == 1: continue
                        move_set.append((p_id,v_id))

                        delta[max_p] += -len(HyperVertex[v_id])
                        delta[p_id] += len(HyperVertex[v_id])
                        break
                
                printInfo(part_vertex,part_edge)
                if len(move_set) == 0 : break
                # print("max_p:",max_p," min_p:",min_p," v_id:",move_set[0])
                test_cnt = 0
                for p_id,v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        part_edge[max_p][e_id] -= 1
                        if part_edge[max_p][e_id] == 0:
                            comm[max_p] -= cross_edge[e_id] - 1
                            test_cnt += cross_edge[e_id] - 1
                            cross_edge[e_id] -= 1
                            part_edge[max_p].pop(e_id)
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    # if p_id == max_p: print("find error")
                                    comm[p_id] -= 1
                
                for min_p,v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        if e_id not in part_edge[min_p].keys():
                            cross_edge[e_id] += 1
                            comm[min_p] += cross_edge[e_id] - 1
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    comm[p_id] += 1
                            part_edge[min_p][e_id] = 0
                        part_edge[min_p][e_id] += 1
                
                for min_p,v_id in move_set:
                    Partition[v_id] = min_p
                    # print("max_p:",max_p," p_id:",Partition[v_id]," v_id:",v_id)
                    part_vertex[max_p].remove(v_id)
                    part_vertex[min_p].add(v_id)
            print("optimation 1:",int((time.time()-beg_time)*100)/100,"(s)")
            

            beg_time = time.time()

            
            while True :
                lst = sorted(comm.items(),key = lambda x:-x[1])
                move_set = []
                max_p = lst[0][0]
                min_p = -1
                lst = sorted([(i,j)for i,j in part_edge[max_p].items()],key = lambda x:-x[1])
                for e_id,_ in lst:
                    if part_edge[max_p][e_id] > 15 : continue 
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

            while True :
                test_sum1 = 0
                test_sum2 = 0
                lst = sorted(comm.items(),key = lambda x:-x[1])
                move_set = []
                max_p = lst[0][0]
                min_p = -1
                lst = sorted([(i,j)for i,j in part_edge[max_p].items()],key = lambda x:-x[1])
                rec = 0
                for e_id,_ in lst:
                    if part_edge[max_p][e_id] > 15 : continue 
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
                        if cnt == part_edge[max_p][ee_id] and cross_edge[ee_id] !=0: 
                            gain += 2 * cross_edge[ee_id] - 2
                            dic[ee_id] = 0
                    rec = 0
                    for p_id in range(max_p,p):
                        if p_id == max_p: continue
                        loss = 0
                        for ee_id,cnt in dic.items():
                            if ee_id not in part_edge[p_id]:
                                if cross_edge[ee_id] == 0: continue
                                if cnt == 0 :
                                    loss += 2 * cross_edge[ee_id] - 2
                                else : loss += 2 * cross_edge[ee_id]
                                # print("test2:",2 * cross_edge[ee_id] - 2)

                        if gain - loss > rec :
                            rec = gain - loss
                            min_p = p_id
                            # break
                    if min_p != -1 : 
                        print("final:",rec," gain:",gain," loss:",loss," num_edge:",part_edge[min_p][e_id])
                        for v_id in HyperEdge[e_id] :
                            if Partition[v_id] != max_p : continue
                            move_set.append(v_id)
                        break
                
                    
                if min_p == -1 : break
                
                printInfo(part_vertex,part_edge)

                for i in range(len(part_edge)):
                    tmp = 0
                    for e_id in part_edge[i]:
                        tmp += cross_edge[e_id] - 1
                    test_sum1 += tmp

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
                for i in range(len(part_edge)):
                    tmp = 0
                    for e_id in part_edge[i]:
                        tmp += cross_edge[e_id] - 1
                    test_sum2 += tmp

                check(part_edge,cross_edge)

                if test_sum1 - test_sum2 != rec :
                    print("fact:",test_sum1 - test_sum2," predict:",rec)
                    break

            print("optimation 2:",int((time.time()-beg_time)*100)/100,"(s)")

            # beg_time = time.time()
            # while True :
            #     lst = sorted(comm.items(),key = lambda x:-x[1])
            #     move_set = []
            #     max_p = lst[0][0]
            #     min_p = lst[-1][0]
            #     mini_loss = 100000000
            #     sel_eid = -1
            #     for e_id in part_edge[max_p].keys():
            #         # if part_edge[max_p][e_id] > 15 : continue 
            #         # min_p = -1
            #         st = set()
            #         dic = {}
            #         gain = 0
            #         for v_id in HyperEdge[e_id]:
            #             # if v_id not in part_vertex[max_p]: continue
            #             if Partition[v_id] != max_p : continue
            #             if v_id not in HyperEdge.keys() : continue
            #             for edge in HyperVertex[v_id]:
            #                 if edge not in dic.keys() : dic[edge] = 0  
            #                 dic[edge] += 1

            #         for ee_id,cnt in dic.items():
            #             if cnt == part_edge[max_p][ee_id] : 
            #                 # print("test1:",2 * cross_edge[ee_id] - 2)
            #                 gain += cross_edge[ee_id] - 1
            #                 dic[ee_id] = 0

            #         loss = 0
            #         for ee_id,cnt in dic.items():
            #             if ee_id not in part_edge[min_p]:
            #                 if dic[ee_id] == 0:
            #                     loss += cross_edge[ee_id] - 1
            #                 else :
            #                     loss += cross_edge[ee_id]
            #                     gain -= 1
            #         if gain <= 0 : continue
            #         # print("test3:",loss," ",gain)
                    
            #         if loss < mini_loss and comm[min_p] + loss < comm[max_p] - gain:
            #             sel_eid = e_id
            #             mini_loss = loss

            #     if sel_eid == -1 : break

            #     # print("final:",rec," gain:",gain," loss:",loss," num_edge:",len(part_edge[min_p]))
            #     for v_id in HyperEdge[sel_eid] :
            #         if Partition[v_id] != max_p : continue
            #         move_set.append(v_id)
            #         break
                
                    
            #     if min_p == -1 : break
                
            #     printInfo(part_vertex,part_edge)

            #     print("max_p:",max_p," min_p:",min_p," mini_loss:",mini_loss)
            #     test_cnt = 0
            #     for v_id in move_set:
            #         # print("v part:",Partition[v_id])
            #         for e_id in HyperVertex[v_id]:
            #             # print(part_edge[max_p].keys())
            #             if e_id not in part_edge[max_p].keys():
            #                 print("error! e_id:",e_id," p_id:",max_p)
            #         for e_id in HyperVertex[v_id]:
            #             part_edge[max_p][e_id] -= 1
            #             if part_edge[max_p][e_id] == 0:
            #                 comm[max_p] -= cross_edge[e_id] - 1
            #                 test_cnt += cross_edge[e_id] - 1
            #                 cross_edge[e_id] -= 1
            #                 part_edge[max_p].pop(e_id)
            #                 # if e_id in part_edge[max_p].keys() : print("__________________________________________")
            #                 for p_id in range(p):
            #                     if e_id in part_edge[p_id].keys():
            #                         # if p_id == max_p: print("find error")
            #                         comm[p_id] -= 1
            #     # print("test_cnt:",test_cnt)
                
            #     for v_id in move_set:
            #         for e_id in HyperVertex[v_id]:
            #             if e_id not in part_edge[min_p].keys():
            #                 cross_edge[e_id] += 1
            #                 comm[min_p] += cross_edge[e_id] - 1
            #                 for p_id in range(p):
            #                     if e_id in part_edge[p_id].keys():
            #                         # if p_id == max_p : print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #                         comm[p_id] += 1
            #                 part_edge[min_p][e_id] = 0
            #             part_edge[min_p][e_id] += 1
                
            #     for v_id in move_set:
            #         Partition[v_id] = min_p
            #         part_vertex[max_p].remove(v_id)
            #         part_vertex[min_p].add(v_id)
                
            # print("optimation 3:",int((time.time()-beg_time)*100)/100,"(s)")

            printInfo(part_vertex,part_edge)
            break
        print("output:",max(comm.values())," ",min(comm.values()))