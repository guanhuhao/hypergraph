
            # while True :
            #     lst = sorted(comm.items(),key = lambda x:-x[1])
            #     move_set = []
            #     max_p = lst[0][0]
            #     min_p = -1
            #     lst = sorted([(i,j)for i,j in part_edge[max_p].items()],key = lambda x:x[1])
            #     # for e_id,_ in lst:
            #     for e_id in part_edge[max_p].keys():
            #         if part_edge[max_p][e_id] > 15 : continue 
            #         min_p = -1
            #         st = set()
            #         dic = {}
            #         gain = 0
            #         for v_id in HyperEdge[e_id]:
            #             # if v_id not in part_vertex[max_p]: continue
            #             if Partition[v_id] != max_p : continue
            #             st.add(v_id)
            #             if v_id not in HyperEdge.keys() : continue
            #             for edge in HyperVertex[v_id]:
            #                 if edge not in dic.keys() : dic[edge] = 0  
            #                 dic[edge] += 1

            #         for ee_id,cnt in dic.items():
            #             if cnt == part_edge[max_p][ee_id] : 
            #                 # print("test1:",2 * cross_edge[ee_id] - 2)
            #                 gain += 2 * cross_edge[ee_id] - 2
            #                 dic[ee_id] = 0
            #         rec = 0
            #         for p_id in range(max_p,p):
            #             if p_id == max_p: continue
            #             loss = 0
            #             for ee_id,cnt in dic.items():
            #                 if ee_id not in part_edge[p_id]:
            #                     if cnt == 0 :
            #                         loss += 2 * cross_edge[ee_id] - 2
            #                     else : loss += 2 * cross_edge[ee_id]
            #                     # print("test2:",2 * cross_edge[ee_id] - 2)

            #             if gain - loss > rec :
            #             # tmp = [i for i in comm]

            #             # if comm[max_p] - gain/2 > comm[p_id] + loss/2 :
            #                 # print("dict:",dic)
            #                 rec = gain - loss
            #                 min_p = p_id
            #                 break
            #         if min_p != -1 : 
            #             print("final:",rec," gain:",gain," loss:",loss," num_edge:",len(part_edge[min_p]))
            #             for v_id in HyperEdge[e_id] :
            #                 if Partition[v_id] != max_p : continue
            #                 move_set.append(v_id)
            #             break
                
                    
            #     if min_p == -1 : break
                
            #     printInfo(part_vertex,part_edge)

            #     print("max_p:",max_p," min_p:",min_p," v_id:",move_set[0])
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

                
            #     # break
        