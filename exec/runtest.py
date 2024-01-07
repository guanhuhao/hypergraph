import os
import re
import math
import time 
import pytz
import datetime

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_list = [
    # "wiki_new.txt",        "wiki_new.txt-swap.txt",\
    # "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",         #  "out.github-swap.txt",\
    # # # # "out.actor-movie",      "out.actor-movie-swap.txt",\
    # # # # "out.dbpedia-team",       "out.dbpedia-team-swap.txt",\
    "out.dblp-author",    #  "out.dblp-author-swap.txt",\
    # # "reuters.txt",        #  "reuters-swap.txt",\
    "out.trackers",     #  "out.trackers-swap.txt",\
    # # #"out.orkut-groupmemberships", 
    "out.orkut-groupmemberships-swap.txt",\
    "enwiki.txt", # "enwiki-swap.txt"\
    ]
# method_list = ["basic","anti-basic","entropy","MinMax","HYPE","KaHyPar","random","NoPar"]
# method_list = ["basic","anti-basic","entropy","MinMax","HYPE","random","NoPar"]
# method_list = ["KaHyPar"]
method_list = ["entropy"]
# method_list = ["BiPart"]
# method_list = ["entropy","HYPE","KaHyPar"]
cur_path = current_path + "/../data/"
os.chdir(current_path)
generate_scheme = False
sheild = 0.2

def log(content):
    import time
    import pytz
    import datetime

    timestamp = datetime.datetime.now()
    desired_timezone = pytz.timezone('Asia/Shanghai')
    localized_time = desired_timezone.localize(timestamp)
    formatted_time = localized_time.strftime("%Y-%m-%d %H:%M:%S\t")

    print(formatted_time + ": " + content)

def pre_KaHyPar(path, dataset):
    edges = {}
    dic_n = set()
    dic_e = set()
    with open(path+dataset,"r") as f: # transform data into suitable format
        for line in f:
            u,v = re.split(" |\t",line[0:-1])[0:2]
            u = int(u)
            v = int(v)

            dic_n.add(u)
            dic_e.add(v)

            if edges.get(v) == None : edges[v] = []
            edges[v].append(u)
            
    with open("./KaHyPar-mid-data","w") as f:
        f.write(str(max(dic_e))+" "+str(max(dic_n))+"\n")
        for i in range(max(dic_e)):
            if edges.get(i) == None : edges[i] = [1]
            for j in range(len(edges[i])):
                if j!=0: f.write(" "+str(edges[i][j]))
                else : f.write(str(edges[i][j]))
            f.write("\n")

def run_KaHyPar(path, dataset, p, generate_scheme=False):
    cmd = "stdbuf -o0 /bin/time -v ./KaHyPar -h ./KaHyPar-mid-data -k " + str(p) +" -e 0.03 -o km1 -m direct -p ./config/km1_kKaHyPar_sea20.ini -w true  > KaHyPar.log 2>&1" # run partition algorithm
    log(cmd)
    os.system(cmd)

    content = open("./KaHyPar.log","r").read() # analyze and record partition time/quaility 
    result = open("result-KaHyPar.txt","a")
    with open("./KaHyPar-mid-data","r") as f:
        m,n = f.readline()[0:-1].split(" ")
    
    if p == 2:
        result.write("\ndata_set:" + dataset + " n:" + n + " m:" + m + "\n")
        result.write(" p , k-1 , partition time , total time  \n")

    k_1 = re.match("(.*)\(k-1\)          \(minimize\) = (\d+)",content,flags=re.S).group(2)
    partition_time = "None"
    total_time = re.match("(.*)Partition time                     = ([-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+))",content,flags=re.S).group(2)
    total_time = str(int(float(total_time)*1000))
    memory_cost = re.match("(.*)Maximum resident set size \(kbytes\): (\d+)",content,flags=re.S).group(2)
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + ","+ memory_cost + "\n")
    result.flush()
    result.close()

    if generate_scheme == True:
        scheme_path = "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/KaHyPar.txt" # generate partition scheme
        result_file = open(scheme_path,"w")
        result_file.close()

        result_file = open(scheme_path,"a")
        with open("KaHyPar-mid-data.part"+str(p)+".epsilon0.03.seed-1.KaHyPar","r") as f:
            ll = 1
            for line in f: 
                par = int(line)
                result_file.write(str(ll)+" "+str(par)+"\n")
                ll += 1

    os.system("rm *KaHyPar-mid-data.*")

def run_HYPE(path, dataset, p, generate_scheme=False):
    print("path:",path,"  dataset:",dataset)
    # print("dataset:",dataset)
    out_path = "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/HYPE.txt"
        
    os.system("rm "+path+"*partition*")
    cmd = "stdbuf -o0 /bin/time -v ./HYPE -f bipartite -i "+ path + dataset +" -p " + str(p) + " -o" +" > HYPE.log 2>&1" # run HYPE partition algorithm
    log(cmd)
    os.system(cmd)

    result = open("result-HYPE.txt","a")     # analyze and record partition time/quaility 
    content = open("./HYPE.log","r").read()
    if p == 2:
        n = re.match("(.*)#Nodes:\s(\d+)",content,flags=re.S).group(2)
        m = re.match("(.*)#HyperEdges:\s(\d+)",content,flags=re.S).group(2)
        result.write("\ndata_set:" + dataset + " n:" + str(n) + " m:" + str(m) + "\n")
        result.write(" p , k-1 , partition time , total time  \n")

    k_1 = re.match("(.*)K-1:\s(\d+)",content,flags=re.S).group(2)
    partition_time = re.match("(.*)partition time:\s(\d+)",content,flags=re.S).group(2)
    total_time = re.match("(.*)total time:\s(\d+)",content,flags=re.S).group(2)
    memory_cost = re.match("(.*)Maximum resident set size \(kbytes\): (\d+)",content,flags=re.S).group(2)
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + ","+ memory_cost + "\n")
    result.flush()
    result.close()


    if generate_scheme == True:                 # generate partition scheme
        directory_path = os.path.dirname(out_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


        scheme_file = open(out_path,"w")
        scheme_file.close()
        scheme_file = open(out_path,"a")
        for outfile in os.listdir(path):
            if re.match("(.*)_partition_(.*)",outfile) == None : continue
                    
            name = re.match("(.*)_partition_(.*)",outfile)[1]
            p_id = re.match("(.*)_partition_(.*)",outfile)[2]

            # print("solving ",name," ",p_id)
            with open(path+"/"+outfile,"r") as f:
                cnt = 0
                for line in f:
                    # 匹配整数或浮点数
                    pattern = re.compile(r'\d+(\.\d+)?')
                    matches = pattern.search(line)
                    if matches == None : continue
                    cnt += 1
                    # if cnt <= 2 : continue
                    scheme_file.write(line[0:-1]+" "+str(p_id)+"\n")
        scheme_file.close()

def run_Our(method,n,m, path, dataset, p, sheild, generate_scheme=False):
    path = "../data/" + dataset
    if generate_scheme : 
        savePath = "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/"+method+".txt"
        directory_path = os.path.dirname(savePath)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    else : 
        savePath = "None"

    cmd =   "stdbuf -o0 /bin/time -v ./cmd-select "+" -n " + str(n) + " -m " + str(m) + " -i " + str(path) + " -p " + str(p) +\
            " -method " + str(method) + " -sheild " + str(sheild)  + " -save "+ savePath + " > cmd.log 2>&1"  # run HYPE partition algorithm
    log(cmd)
    os.system(cmd)

    result = open("result-"+method+".txt","a")     # analyze and record partition time/quaility 
    content = open("./cmd.log","r").read()
    if p == 2:
        result.write("\ndata_set:" + dataset + " n:" + str(n) + " m:" + str(m) + "\n")
        result.write(" p , k-1 , partition time , total time  \n")
    k_1 = re.match("(.*)k-1:(\d+)",content,flags=re.S).group(2)
    partition_time = re.match("(.*)runtime:(\d+)",content,flags=re.S).group(2)
    total_time = re.match("(.*)runtime:(\d+)",content,flags=re.S).group(2)
    memory_cost = re.match("(.*)Maximum resident set size \(kbytes\): (\d+)",content,flags=re.S).group(2)
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + ","+ memory_cost + "\n")
    result.flush()
    result.close()

def run_MinMax(path,dataset,n,m,p, generate_scheme=False):
    path = path + dataset 
    if generate_scheme : 
        savePath = "/back-up/large-cluster/comm/test_data/"+str(p)+"/"+dataset+"/"+method+".txt"
        directory_path = os.path.dirname(savePath)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    else : 
        savePath = "None"

    cmdd = " -i " + path +" -n " + str(n) + " -m " + str(m) + " -p " + str(p) + " -save " + savePath 
    os.system("stdbuf -o0 /bin/time -v ./MinMax-pre " + cmdd + " > MinMax.log 2>&1")
    log("stdbuf -o0 /bin/time -v  ./MinMax-main " + cmdd + " > MinMax.log 2>&1" )
    os.system("stdbuf -o0 /bin/time -v  ./MinMax-main " + cmdd + " > MinMax.log 2>&1" )

    result = open("result-MinMax.txt","a")     # analyze and record partition time/quaility 
    content = open("./MinMax.log","r").read()
    if p == 2:
        result.write("\ndata_set:" + dataset + " n:" + str(n) + " m:" + str(m) + "\n")
        result.write(" p , k-1 , partition time , total time  \n")
    k_1 = re.match("(.*)k-1: (\d+)",content,flags=re.S).group(2)
    partition_time = re.match("(.*)runtime: (\d+)",content,flags=re.S).group(2)
    total_time = re.match("(.*)runtime: (\d+)",content,flags=re.S).group(2)
    memory_cost = re.match("(.*)Maximum resident set size \(kbytes\): (\d+)",content,flags=re.S).group(2)
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + ","+ memory_cost + "\n")
    result.flush()
    result.close()

def run_NoPar(path,dataset):
    print("path:",path,"  dataset:",dataset)
    vertex_info = "/back-up/large-cluster/comm/test_data/"+str(2)+"/"+dataset+"/vertex_info.txt"
    out_path = "/back-up/large-cluster/comm/test_data/1/"+dataset+"/NoPar.txt"
    directory_path = os.path.dirname(out_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    w = open(out_path,"w")

    with open(vertex_info,"r") as file :
        for line in file:
            vid = line.split()[0]
            w.write(vid+" 0\n")

def run_BiPart(path, dataset, n, m, p, generate_scheme=False):
    opt = "" 
    balance = p/n * 2 * 100
    if balance < 0.001 : balance = "0.001"
    if generate_scheme == True:
        opt = " --output --outputFile=test" 

    cmd = "stdbuf -o0 /bin/time -v ./bipart-cpu -hMetisGraph -t 10 --balance="+ str(balance) + opt + \
          " ./KaHyPar-mid-data 25 2 "+str(p) + " > BiPart.log 2>&1"
    log(cmd)
    os.system(cmd)

    content = open("./BiPart.log","r").read() # analyze and record partition time/quaility 
    result = open("result-BiPart.txt","a")
    if p == 2:
        result.write("\ndata_set:" + dataset + " n:" + str(n) + " m:" + str(m) + "\n")
        result.write(" p , k-1 , partition time , total time  \n")

    k_1 = re.match("(.*)Edge Cut,(\d+)",content,flags=re.S).group(2)
    partition_time = "None"
    total_time = re.match("(.*)total time:([-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+))",content,flags=re.S).group(2)
    memory_cost = re.match("(.*)Maximum resident set size \(kbytes\): (\d+)",content,flags=re.S).group(2)
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + ","+ memory_cost + "\n")
    result.flush()
    result.close()


# os.system("rm *result-*")
for method in method_list:
    path = "../data/"

    for dataset in dataset_list:
        if method == "NoPar":
            run_NoPar(path,dataset)
            continue
        n = 0
        m = 0
        with open("../data/"+dataset) as file:
            for line in file:
                a,b = line.split()
                n = max(n,int(a)+1)
                m = max(m,int(b)+1)
        p = 1

        if(method == "MinMax"):
            cmdd = " -i " + path + dataset  +" -n " + str(n) + " -m " + str(m) + " -p " + str(p) 
            os.system("stdbuf -o0 /bin/time -v ./MinMax-pre " + cmdd + " > MinMax.log 2>&1")
        if(method == 'KaHyPar' or method == 'BiPart'):
            pre_KaHyPar(path, dataset)

        while p < 256:
            p *= 2

            timestamp = datetime.datetime.now()
            desired_timezone = pytz.timezone('Asia/Shanghai')
            localized_time = desired_timezone.localize(timestamp)
            formatted_time = localized_time.strftime("%Y-%m-%d %H:%M:%S\t")
          
            # print(formatted_time + " dataset:" + dataset + " p:" + str(p))

            # continue

            if method == "KaHyPar"  :   
                if dataset !=  "out.github" and dataset !=  "out.dblp-author" :
                    continue
                run_KaHyPar(path,dataset,p,generate_scheme)
            elif method == "HYPE"   :   
                run_HYPE(path,dataset,p,generate_scheme)
            elif method == "basic" or method == "anti-basic" or method == "entropy" or method == "random" :
                run_Our(method,n,m, path, dataset, p, sheild, generate_scheme)
            elif method == "MinMax" :
                run_MinMax(path,dataset,n,m,p,generate_scheme)
            elif method == "BiPart" :
                run_BiPart(path, dataset, n, m, p, generate_scheme)
            # break