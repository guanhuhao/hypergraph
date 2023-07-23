from multiprocessing import Process,Queue
import time
# from multiprocessing import JoinableQueue as Queue
# import multiprocessing.JoinableQueue as Queue
import os
import sys

INF = 1e9
SourceNode = 1

class HyperNode:
    def __init__(self,n_id,edges):
        self.n_id = n_id
        self.value = INF 
        self.edges = edges
        
    def AddEdge(self,edge):
        self.edges.append(edge)
        
    def GetHyperEdges(self):
        return self.edges
    
    def GetValue(self):
        return self.dist
    
                    
class HyperEdge:
    def __init__(self,e_id,nodes,cross=set() ):
        self.e_id = e_id
        self.nodes = nodes
        self.cross = cross
#         self.value = 1
        
    def AddNode(self,node):
        self.nodes.append(node)
    
    def GetHyperNodes(self):
        return self.nodes
    
    def getValue(self):
        return self.e_id%5 + 1

def aggregate(msg):
    dic = {}
    for tar,value in msg:
        if tar not in dic :
            dic[tar] = INF
        dic[tar] = min(dic[tar],value)
    return [(tar,value) for tar,value in dic.items() ]

class Master:
    def __init__(self,p):
        self.p = p
        self.Node = {}
        self.Edge = {}
        self.cross = {}
        self.Part = {}
        self.Worker = []
        
        self.thread_pool = []
        self.m2sPipe = []
        self.s2mPipe = []
        self.recvBuf = [Queue() for i in range(p)]
        
        self.result = {}
        for i in range(p) :
            self.Worker.append(Worker(i))
            self.m2sPipe.append(Queue())
            self.s2mPipe.append(Queue())
            
        for worker in self.Worker:
            w_id = worker.w_id
            self.thread_pool.append(Process(target= worker.run,args=(self.m2sPipe[w_id],self.s2mPipe[w_id],self.recvBuf)))

    def terminal(self):
#         sys.stdout.write("begin terminal function!")
        for pipe in self.m2sPipe:
            while not pipe.empty():
                pipe.get()
            pipe.close()
            
        for pipe in self.s2mPipe:
            while not pipe.empty():
                pipe.get()
            pipe.close()
            
        for buf in self.recvBuf:
            while not buf.empty():
                buf.get()
            buf.close()
            
        sys.stdout.write("before join!\n")
        for thread in self.thread_pool:
            thread.terminate()
        sys.stdout.write("OKK!\n")
            
            
    def load_data(self,data_file,par_method = "partition_method.txt"):
        data_path = "../data/"
        file_path = "./test_data/"+str(self.p)+"/"+data_file+"/"
        print("dataset:",data_file," partition method:"+par_method);
        with open(file_path+par_method) as file :  # (n_id,p_id)
            for line in file:
                v_id,par_id = line[0:-1].split(" ")
                v_id,par_id = int(v_id),int(par_id)
                self.Part[v_id] = par_id
                self.Node[v_id] = []
                    
        with open(file_path+"vertex_info.txt") as file:  # v_id, e1_id, e2_id, ...
            for line in file:
                data = line[0:-1].split(" ")
                v_id = int(data[0])
                self.Node[v_id] = [int(i) for i in data[1:]]
                    
        with open(file_path+"edge_info.txt") as file:   # e_id, v1_id, v2_id,...
            for line in file:
                data = line[0:-1].split(" ")
                e_id = int(data[0])
                self.Edge[e_id] = [int(i) for i in data[1:]]

    def sync(self):
        return [sign.get()  for sign in self.s2mPipe]
    
    def broadcast(self,signal=0):
#         sys.stdout.write("signal "+str(signal)+"\n")
        for m2sPipe in self.m2sPipe:
                m2sPipe.put(signal)
            
    def distribute_node(self):
        for n_id,p_id in self.Part.items():
#             print("debug:",p_id)
            self.m2sPipe[p_id].put((n_id,self.Node[n_id]))
        for m2sPipe in self.m2sPipe:
            m2sPipe.put((-1,[-1]))

        self.sync()
#         self.Worker[w_id].Node[n_id] = self.Node[n_id]
    
    def distribute_edge(self):
        for e_id,node in self.Edge.items():
            cross_set = set()
            for n_id in node :
                p_id = self.Part[n_id]
                if len(cross_set) == self.p : break
                cross_set.add(p_id)
            for p_id in cross_set:
                if e_id not in self.cross : 
                    self.cross[e_id] = set()
                self.cross[e_id].add(p_id)
                self.m2sPipe[p_id].put((e_id,node,cross_set))
                
        for m2sPipe in self.m2sPipe:
            m2sPipe.put((-1,[-1],set()))
            
        self.sync()
    
    def distribute_part(self):
        for worker in self.Worker:
            for item in self.Part.items():
                self.m2sPipe[worker.w_id].put(item)
            self.m2sPipe[worker.w_id].put((-1,-1))
            
            
        self.sync()
        
    def distribute(self):
        self.distribute_part()
        self.distribute_node()
        self.distribute_edge()
        
    def get_result(self):
        cnt = 0

        for pipe in self.s2mPipe: 
            while True:
                v_id,dist  = pipe.get()
#                 sys.stdout.write("update dist:"+ str(v_id)+" "+str(dist))
                if v_id == -1: 
                    break
                self.result[v_id] = dist
        # sys.stdout.write("get result !\n")
        
        
        

    def run(self):
        for thread in self.thread_pool:
            thread.start()
#         sys.stdout.write("All thread start"+"\n")
        distribute_beg = time.time()
        self.distribute()
        distribute_time = ((time.time() - distribute_beg)*100000)/100
        print("distribute time:",distribute_time,"ms")
#         sys.stdout.write("init data distribute over"+"\n")
        
        msg_num = 1
        turn = 0
        
#         source_id = 1 # init status
#         self.recvBuf[self.Part[source_id]].put((source_id,0,0))
        for e_id,edge in self.Edge.items():
            for p in self.cross[e_id]:
                self.recvBuf[p].put((e_id,1,0))
        for buf in self.recvBuf:
            for i in range(1,self.p+1):
#                 print(-i)
                buf.put((-i,-i,-i))
#         sys.stdout.write("master edge num:"+str(len(self.Node[source_id])))
        
#         communicate_beg = time.time()
        msg_tot = 0
        msg_cro = 0
        msg_max = 0
        compute_time = 0
        communicate_time = 0
        send_time = 0
        recv_time = 0
        while msg_num != 0 and turn < 30:   
            turn += 1
            # sys.stdout.write("---------------\n"+"turn:"+str(turn)+"\n")
#             sys.stdout.write("beign turn:"+str(turn)+"\n")

            communicate_beg = time.time()
            self.broadcast(0) # begin recevie buffer 
            msg = self.sync() # wait finish recevie buffer
#             print('communicate time:%s(ms)' % (int((time.time() - communicate_beg)*100000)/100))
            recv_time += int((time.time() - communicate_beg)*100000)/100
#             sys.stdout.write("receive buffer info ok"+"\n")
            
            compute_beg = time.time()
            self.broadcast(0) # begin compute
            msg = self.sync() # wait finish compute
#             print('compute time:%s(ms)' % (int((time.time() - compute_beg)*100000)/100))
            compute_time += int((time.time() - compute_beg)*100000)/100
    
            communicate_beg = time.time()
            self.broadcast(0) # begin send buffer 
            msg = self.sync() # wait finish send buffer
#             print('communicate time:%s(ms)' % (int((time.time() - communicate_beg)*100000)/100))
            send_time += int((time.time() - communicate_beg)*100000)/100
            
            
            
#             sys.stdout.write("compute ok"+"\n")
            msg_num = sum([item[0] for item in msg])
            cro_num = sum([item[1] for item in msg])
            
            msg_tot += msg_num
            msg_max += max([item[0] for item in msg])
            msg_cro += cro_num
#             sys.stdout.write("total msg:"+str(msg_num)+" cross_msg:"+str(cro_num)+"\n")
#             sys.stdout.write("detai msg:"+str([item[0] for item in msg])+"\n")
                
            self.get_result()
    
#             dic = {}
#             for key in range(5): 
#                 dic[key] = 0
#             for key,value in self.result.items():
#                 if value not in dic :
#                     dic[value] = 0
#                 dic[value] += 1
#             for key in range(5):
#                 print(key,":",dic[key])
        
        sys.stdout.write("terminal "+"\n")
        self.broadcast(-1) # off worker
#         self.sync()
#         sys.stdout.write("wokers shut down"+"\n")
            
        self.get_result()
        self.terminal()
        
        sys.stdout.write("finished"+"\n")
        print("msg info:\ntotal msg:",msg_tot,\
              " cross msg:",msg_cro,\
              " sum of max msg:",msg_max,\
              "\ntime info:\ncompute time:",int(compute_time*100)/100,\
              "(ms) communicate time:",int((send_time+recv_time)*100)/100,\
              "(ms)\nsend time:",int(send_time*100)/100,\
              "(ms) recv time:",int(recv_time*100)/100,\
              "(ms)\ntotal time:",int(send_time*100+recv_time*100+compute_time*100)/100
             )
        return {"total_msg":str(msg_tot),\
                "cross_msg":str(msg_cro),\
                "distribute_time":str(int(distribute_time*100)/100),\
                "compute_time":str(int(compute_time*100)/100),\
                "communicate_time":str(int((send_time+recv_time)*100)/100),\
                "send_time":str(int(send_time*100)/100),\
                "recv_time":str(int(recv_time*100)/100),\
                "total_time":str(int(send_time*100+recv_time*100+compute_time*100)/100)
               }
      
    def n2n_single_metric(self):
        cnt = 0
        for n_id,edges in self.Node.items():
            nei = set()
            for e_id in edges:
                for node in self.Edge[e_id]:
                    if self.Part[n_id] != self.Part[node]:
                        cnt += 1
        return cnt
    
    def n2n_agg_metric(self):
        cnt = 0
        for n_id,edges in self.Node.items():
            nei = set()
            for e_id in edges:
                for node in self.Edge[e_id]:
                    nei.add(node)
            for node in nei:
                if self.Part[n_id] != self.Part[node]:
                    cnt += 1
        return cnt
          
class Worker:
    def __init__(self,w_id):
        self.w_id = w_id
        self.Node = {}
        self.Edge = {}
        self.Part = {}
        self.msg = {}
        self.sendBuf = []
        self.recvBuf = []
        filepath = "./pipeline/"+str(self.w_id)
        open(filepath,"w")
        self.turn = 0

    def cal_node(self,node):
        msgs = self.msg[node.n_id]
        mindist = INF 
        mindist = min(msgs)
        sendMessage = []
        if mindist < node.dist : 
            node.dist = mindist
            
            for e_id in node.GetHyperEdges():
#                 print("debug:",self.w_id," ",e_id)
                hyperEdge = self.Edge[e_id]
                for n_id in hyperEdge.GetHyperNodes():
                    sendMessage.append((n_id,mindist+hyperEdge.getValue()))
#                     SendMessageTo(self.v_id,target,mindist+hyperEdge.getValue())
        return sendMessage
    
    def receive_node(self,m2sPipe,s2mPipe):
        while True:
            v_id,edge = m2sPipe.get()
            
            if v_id == -1 : break
            if v_id in self.Node : 
                continue
            self.Node[v_id] = HyperNode(v_id,edge)

        s2mPipe.put(self.w_id)

        
    def receive_edge(self,m2sPipe,s2mPipe):
        while True:
            e_id,node,cross = m2sPipe.get()
            if e_id == -1 : break
            if e_id in self.Edge : 
                continue
            self.Edge[e_id] = HyperEdge(e_id,node,cross)
        s2mPipe.put(self.w_id)
#         print(self.w_id," edge_num:",len(self.Edge))
        
        
    def receive_part(self,m2sPipe,s2mPipe):
        while True:
            v_id,p_id = m2sPipe.get()
            if v_id == -1 : break
            self.Part[v_id] = p_id
#             if len(self.Part)%10000 == 0 :
#                 print(self.w_id," ",len(self.Part))
        s2mPipe.put(self.w_id)
            

    def run(self,m2sPipe,s2mPipe,sendBuf):
        self.receive_part(m2sPipe,s2mPipe)
        self.receive_node(m2sPipe,s2mPipe)
        self.receive_edge(m2sPipe,s2mPipe)
        
        while True:
            self.turn += 1
            sig = m2sPipe.get()
#             sys.stdout.write("w_id:"+str(self.w_id)+" sign:"+str(sig)+"\n")
            if sig == -1 : 
                break
            self.receiveMsg(s2mPipe,sendBuf)
            
            m2sPipe.get()
            msg = self.compute(s2mPipe,sendBuf) 
            
            m2sPipe.get()
            self.sendMsg(msg,s2mPipe,sendBuf)
            
#         sys.stdout.write("w_id:"+str(self.w_id)+" test "+str(len(self.Node))+"\n")
            for node in self.Node.values():
                s2mPipe.put((node.n_id,node.value))
#         sys.stdout.write("w_id:"+str(self.w_id)+" send result"+"\n")
            s2mPipe.put((-1,-1))
    
        for node in self.Node.values():
            s2mPipe.put((node.n_id,node.value))
        s2mPipe.put((-1,-1))
        # sys.stdout.write("worker "+str(self.w_id)+" finished!\n")
        return 
    
    def sendMsg(self,flag,s2mPipe,Buffer):
        msg = {}
        for e_id,edge in self.Edge.items():
            msg[e_id] = 0
            for n_id in edge.nodes:
                if self.Part[n_id] != self.w_id : continue
                msg[e_id] +=  self.Node[n_id].value / len(self.Node[n_id].edges)
                    
        msg_cnt = 0
        cross_cnt = 0
#         sys.stdout.write("!!: "+str(len(msg.items()))+"\n")
#         if 
#         sys.stdout.write("w_id "+str(self.w_id)+" "+str(len(msg.items()))+"\n")
        for e_id,value in msg.items():   # send msg
            for p_id in self.Edge[e_id].cross:
                msg_cnt += 1
                if p_id == self.w_id : 
                    self.recvBuf.append((e_id,value,self.turn))
                else :
                    cross_cnt += 1
                    Buffer[p_id].put((e_id,value,self.turn))
                    
        for i in range(len(Buffer)):
             Buffer[i].put((-self.w_id-1,-self.w_id-1,-self.w_id-1))   
#         sys.stdout.write("debug: "+str(msg_cnt)+" "+str(cross_cnt)+"\n")
        if flag == 0 : s2mPipe.put((0,0))
        else : s2mPipe.put((msg_cnt,cross_cnt))
        
    def receiveMsg(self,s2mPipe,Buffer):
        self.msg = {}
        cnt = 0
        for e_id in self.Edge.keys():
            self.Edge[e_id].value = 0
        while True:
            tar,value,turn = Buffer[self.w_id].get()
#             sys.stdout.write("test2: "+str(tar)+" "+str(value)+" "+str(turn)+"\n")
            if tar < 0 :
                cnt += 1
                if cnt == len(Buffer) : break
                else : continue
                
            self.Edge[tar].value += value 
#             self.msg[tar].append(value)
            
        for tar,value,turn in self.recvBuf:
            self.Edge[tar].value += value 
        self.recvBuf = []
        
        
        s2mPipe.put(self.w_id)
        
    def compute(self,s2mPipe,Buffer):
        flag = 0
        for n_id,node in self.Node.items():
            PR_score = 0
            for e_id in node.edges:
#                 if (len(self.Edge[e_id].nodes)-1) <= 0 : continue
                PR_score += (1 - alpha) * self.Edge[e_id].value/(len(self.Edge[e_id].nodes))
            PR_score += alpha
#             if PR_score <= 0 : continue
            if abs(PR_score - self.Node[node.n_id].value) / PR_score < 0.01 :
                continue
            flag += 1
            self.Node[node.n_id].value = PR_score
            
#         sys.stdout.write("flag cnt: "+str(self.w_id)+" "+str(flag)+"\n")
        
        s2mPipe.put((-1,-1))    
        
        return flag
                

# data_file = "wiki"
# data_file = "location"
# data_file = "github"
# data_file = "author"

# master = Master(16)
# master.load_data("NA.txt")
# master.load_data("MinMax.txt")
# master.load_data("HYPE.txt")
# master.run()

import re
data_path = os.getcwd()+"/../data/"
os.system("rm "+data_path+"*partition*")

method = ["NA.txt","HYPE.txt","MinMax.txt"]

alpha = 0.15
for mm in method:
    result = open(mm+"-result.txt","w")

for file in os.listdir(data_path):
    if re.match("(.*)ipynb(.*)",file) != None : continue
    if os.path.isdir(data_path+file) == True : continue
    if re.match("(.*)orkut(.*)",file) != None : continue
    if re.match("(.*)tracker(.*)",file) != None : continue
    if re.match("(.*)rand(.*)",file) != None : continue
    if re.match("(.*)author(.*)",file) != None : continue

    # if re.match("(.*)wiki(.*)",file) == None : continue

    for mm in method:
        print("---------------------------\nsolving ",file," ",mm)

        p = 1
        data_file = file        

        while p < 64:
            p *= 2
            master = Master(p)
            master.load_data(file,mm)
            dic = master.run()        


            result = open(mm+"-result.txt","a")
            if p == 2:
                result.write("\ndataset:"+file+" n:"+str(len(master.Node))+" m:"+str(len(master.Edge))+"\n")
                result.write("p,total_msg,cross_msg,distribute_time,compute_time,communicate_time,send_time,recv_time,total_time\n")
#             print(master.p)
            
            result.write(str(p)+", "+\
                    str(dic["total_msg"])+", "+\
                    str(dic["cross_msg"])+", "+\
                    str(dic["distribute_time"])+", "+\
                    str(dic["compute_time"])+", "+\
                    str(dic["communicate_time"])+", "+\
                    str(dic["send_time"])+", "+\
                    str(dic["recv_time"])+", "+\
                    str(dic["total_time"])+"\n"
                   )
            result.close()

