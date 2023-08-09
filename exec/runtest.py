import os
import re
dataset_list = [
    "wiki_new.txt",         "wiki_new.txt-swap.txt",\
    "out.dbpedia-location", "out.dbpedia-location-swap.txt",\
    "out.github",           "out.github-swap.txt",\
    "out.actor-movie",      "out.actor-movie-swap.txt",\
    "out.dbpedia-team",     "out.dbpedia-team-swap.txt",\
    ]
method_list = ["basic","anti-basic","entropy","MinMax","HYPE","KaHyPar","random"]
method_list = ["random"]
cur_path = os.getcwd()+"/../data/"

def run_KaHyPar(path, dataset, p, generate_scheme=False):
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
            
    with open("./KaHypar-mid-data","w") as f:
        f.write(str(max(dic_e))+" "+str(max(dic_n))+"\n")
        for i in range(max(dic_e)):
            if edges.get(i) == None : edges[i] = [1]
            for j in range(len(edges[i])):
                if j!=0: f.write(" "+str(edges[i][j]))
                else : f.write(str(edges[i][j]))
            f.write("\n")

    cmd = "stdbuf -o0 ./KaHyPar -h ./KaHypar-mid-data -k " + str(p) +" -e 0.03 -o km1 -m direct -p ./config/km1_kKaHyPar_sea20.ini -w true  1>./KaHypar.log" # run partition algorithm
    print(cmd)
    os.system(cmd)

    content = open("./KaHypar.log","r").read() # analyze and record partition time/quaility 
    result = open("result-KaHyPar.txt","a")
    with open("./KaHypar-mid-data","r") as f:
        m,n = f.readline()[0:-1].split(" ")
    
    if p == 2:
        result.write("\ndata_set:" + dataset + " n:" + n + " m:" + m + "\n")
        result.write(" p , k-1 , partition time , total time  \n")

    k_1 = re.match("(.*)\(k-1\)          \(minimize\) = (\d+)",content,flags=re.S).group(2)
    partition_time = "None"
    total_time = re.match("(.*)Partition time                     = ([-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+))",content,flags=re.S).group(2)
    total_time = str(int(float(total_time)*1000))
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + "\n")
    result.flush()
    result.close()

    if generate_scheme == True:
        scheme_path = "../simulation/test_data/"+str(p)+"/"+dataset+"/KaHypar.txt" # generate partition scheme
        result_file = open(scheme_path,"w")
        result_file.close()

        result_file = open(scheme_path,"a")
        with open("KaHypar-mid-data.part"+str(p)+".epsilon0.03.seed-1.KaHyPar","r") as f:
            ll = 1
            for line in f: 
                par = int(line)
                result_file.write(str(ll)+" "+str(par)+"\n")
                ll += 1

    os.system("rm *KaHypar-mid-data*")


def run_HYPE(path, dataset, p, generate_scheme=False):
    print("path:",path)
    print("dataset:",dataset)
    out_path = "../simulation/test_data/"+str(p)+"/"+dataset+"/HYPE.txt"
        
    os.system("rm "+path+"*partition*")
    cmd = "stdbuf -o0 ./HYPE -f bipartite -i "+ path + dataset +" -p " + str(p) + " -o" +" 1>./HYPE.log" # run HYPE partition algorithm
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
    result.write(str(p) + "," + k_1 + "," + partition_time + "," + total_time + "\n")
    result.flush()
    result.close()


    if generate_scheme == True:                 # generate partition scheme
        scheme_file = open(out_path,"w")
        scheme_file.close()
        scheme_file = open(out_path,"a")
        for outfile in os.listdir(path):
            if re.match("(.*)_partition_(.*)",outfile) == None : continue
                    
            name = re.match("(.*)_partition_(.*)",outfile)[1]
            p_id = re.match("(.*)_partition_(.*)",outfile)[2]

            print("solving ",name," ",p_id)
            with open(path+"/"+outfile,"r") as f:
                cnt = 0
                for line in f:
                    cnt += 1
                    if cnt <= 2 : continue
                    scheme_file.write(line[0:-1]+" "+str(p_id)+"\n")
        scheme_file.close()


os.system("rm *result-*")
for method in method_list:
    path = "../data/"
    generate_scheme = False

    if method == "basic" or method == "anti-basic" or method == "entropy" or method == "random":
        os.system("./cmd "+method+" 2>result-"+method+".txt")
        continue

    if method == "MinMax":
        os.system("./"+method)
        continue

    for dataset in dataset_list:
        p = 1 
        while p < 64:
            p *= 2
            if method == "KaHyPar"  :   run_KaHyPar(path,dataset,p,generate_scheme)
            elif method == "HYPE"   :   run_HYPE(path,dataset,p,generate_scheme)