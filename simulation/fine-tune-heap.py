from ctypes import sizeof
import heapq
import os
import re
from math import log
def heap_comp(x):
    return -x[1]

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

            heap = [[] for i in range(p)]
            check_heap = [set() for i in range(p)]
            heap_size = 10000
            for i in range(p):
                for e_id,cnt in part_edge[max_p].items():
                    heapq.heappush(heap[i], (heap_comp((e_id,cnt)),(e_id,cnt)))
                    check_heap[i].add(e_id)
                    while len(heap[i]) > heap_size:
                        id,value = heap[i][0][1]
                        heapq.heappop(heap[i])
                        # print("test:",i," ",id," ",value," ",heap[i][0][1])
                        check_heap[i].remove(id)

            while True :
                lst = sorted(comm.items(),key = lambda x:-x[1])
                move_set = []
                max_p = lst[0][0]
                min_p = lst[-1][0]
                mini_loss = 100000000
                sel_eid = -1
                if len(heap[max_p]) > 2 * heap_size :
                    heap[max_p] = []
                    for e_id in check_heap[max_p] :
                        heapq.heappush(heap[i], (heap_comp((e_id,part_edge[e_id])),(e_id,part_edge[e_id])))

                for score,(e_id,_) in heap[max_p]:
                    if part_edge[max_p][e_id] > 50 : continue
                    # print("score:",score," A:",e_id," B:",_)
                    # min_p = -1
                    st = set()
                    dic = {}
                    gain = 0
                    for v_id in HyperEdge[e_id]:
                        # if v_id not in part_vertex[max_p]: continue
                        if Partition[v_id] != max_p : continue
                        if v_id not in HyperEdge.keys() : continue
                        for edge in HyperVertex[v_id]:
                            if edge not in dic.keys() : dic[edge] = 0  
                            dic[edge] += 1

                    for ee_id,cnt in dic.items():
                        if cnt == part_edge[max_p][ee_id] : 
                            # print("test1:",2 * cross_edge[ee_id] - 2)
                            gain += cross_edge[ee_id] - 1
                            dic[ee_id] = 0

                    loss = 0
                    for ee_id,cnt in dic.items():
                        if ee_id not in part_edge[min_p]:
                            if dic[ee_id] == 0:
                                loss += cross_edge[ee_id] - 1
                            else :
                                loss += cross_edge[ee_id]
                                gain -= 1
                    # print("test3:",loss," ",gain)
                    if gain <= 0 : continue
                    
                    if loss < mini_loss and comm[min_p] + loss < comm[max_p] - gain:
                        sel_eid = e_id
                        mini_loss = loss
                        # break
                # print("sel_eid",sel_eid)
                if sel_eid == -1 : break

                # print("final:",rec," gain:",gain," loss:",loss," num_edge:",len(part_edge[min_p]))
                for v_id in HyperEdge[sel_eid] :
                    if Partition[v_id] != max_p : continue
                    move_set.append(v_id)
                    break
                
                    
                if min_p == -1 : break
                
                printInfo(part_vertex,part_edge)

                print("max_p:",max_p," min_p:",min_p," mini_loss:",mini_loss)
                for v_id in move_set:
                    for e_id in HyperVertex[v_id]:
                        part_edge[max_p][e_id] -= 1
                        if len(check_heap[max_p]) < heap_size:
                            check_heap[max_p].add(e_id)
                            heapq.heappush(heap[max_p],(heap_comp((e_id,part_edge[max_p][e_id])),(e_id,part_edge[max_p][e_id])))

                        elif -part_edge[max_p][e_id] > heap[max_p][0][0] and e_id not in  check_heap[max_p]:
                            while heap[max_p][0][1][0] not in check_heap[max_p] : heapq.heappop(heap[max_p])
                            check_heap[max_p].remove(heap[max_p][0][1][0])
                            heapq.heappop(heap[max_p])

                            check_heap[max_p].add(e_id)
                            heapq.heappush(heap[max_p],(heap_comp((e_id,part_edge[max_p][e_id])),(e_id,part_edge[max_p][e_id])))
                        if part_edge[max_p][e_id] == 0:
                            comm[max_p] -= cross_edge[e_id] - 1
                            cross_edge[e_id] -= 1

                            check_heap[max_p].remove(e_id)
                            part_edge[max_p].pop(e_id)
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    comm[p_id] -= 1
                
                for v_id in move_set:
                    rec_dic = set()
                    for e_id in HyperVertex[v_id]:
                        if e_id not in part_edge[min_p].keys():
                            rec_dic.add(e_id)
                            cross_edge[e_id] += 1
                            comm[min_p] += cross_edge[e_id] - 1
                            for p_id in range(p):
                                if e_id in part_edge[p_id].keys():
                                    comm[p_id] += 1
                            part_edge[min_p][e_id] = 0
                        part_edge[min_p][e_id] += 1
                    for e_id in rec_dic:
                        if len(check_heap[min_p]) < heap_size:
                            check_heap[min_p].add(e_id)
                            heapq.heappush(heap[min_p],(heap_comp((e_id,part_edge[min_p][e_id])),(e_id,part_edge[min_p][e_id])))
                        elif -part_edge[min_p][e_id] > heap[min_p][0][0] and e_id not in check_heap[min_p]:
                            while heap[min_p][0][1][0] not in check_heap[min_p] : heapq.heappop(heap[min_p])
                            check_heap[min_p].remove(heap[min_p][0][1][0])
                            heapq.heappop(heap[min_p])

                            check_heap[min_p].add(e_id)
                            heapq.heappush(heap[min_p],(heap_comp((e_id,part_edge[min_p][e_id])),(e_id,part_edge[min_p][e_id])))
                
                for v_id in move_set:
                    Partition[v_id] = min_p
                    part_vertex[max_p].remove(v_id)
                    part_vertex[min_p].add(v_id)

                
                # break
            printInfo(part_vertex,part_edge)
            break
        print("output:",max(comm.values())," ",min(comm.values()))