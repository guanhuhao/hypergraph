import os
import re
import random
cur_path = "../data" #获取当前文件绝对路径
Node = set()
Edge = set()
nodes = {}
p = 8
for file in os.listdir(cur_path):
    if re.match("(.*).ipynb",file) != None : continue
    if(os.path.isdir(file)) : continue
    Node = set()
    Edge = set()
    nodes = {}
    print("solving ",file)
    dic_n = {}
    dic_e = {}
    with open(cur_path+"/"+file,"r") as f:
        for line in f:
            # print(re.split(" |\t",line[0:-1])[0:2])
            n,e = re.split(" |\t",line[0:-1])[0:2]
            if dic_n.get(n) == None : dic_n[n] = len(dic_n) + 1
            if dic_e.get(e) == None : dic_e[e] = len(dic_e) + 1
            u = dic_n[n]
            v = dic_e[e]
            Node.add(u)
            Edge.add(v)
            if nodes.get(u) == None : nodes[u] = []
            nodes[u].append(v)
    with open(cur_path+"/random_par/"+file,"w") as f:
        f.write(str(len(dic_n))+" "+str(len(dic_e))+"\n")
        n = len(dic_n)
        for i in range(1,len(Node)+1):
            for j in range(len(nodes[i])):
                par = random.randint(1,p)
                f.write(str(i)+" "+str(j+n)+" "+str(par)+"\n")
                f.write(str(j+n)+" "+str(i)+" "+str(par)+"\n")