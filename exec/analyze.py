import os 
import re
import pandas as pd


def loadPar():
    dic = {
        "method"    : [],
        "dataset"   : [],
        "p"         : [],
        "k-1"       : [],
        "ParTime"      : []
    }
    dic2 = {}
    path = "./new-result/"
    for filename in os.listdir(path):
        match = re.search(r'result-(.+).txt', filename) 
        if match : 
            print(filename)
            method = match.group(1)
            with open(path+"/"+filename) as file:
                for line in file:
                    match = re.search(r':(.+) n:', line) 
                    if match :
                        dataset = match.group(1)
                    if line[0] > '9' or line[0] < '0' :
                        continue
                    p, k = line[:-1].split(',')[0:2]
                    TotTime = line[:-1].split(',')[-1]
                    dic["method"].append(method)
                    dic["dataset"].append(dataset)
                    dic["p"].append(p)
                    dic["k-1"].append(k)
                    dic["ParTime"].append(TotTime)
                    dic2[(method,dataset,p)] = (k,TotTime)
                    # print(p, k, partTime, TotTime)
    return dic

def loadresult(path,workload,speed):
    check = loadPar()
    dic = {
        "workload"  : [],
        "method"    : [],
        "dataset"   : [],
        "speed"     : [],
        "p"         : [],
        "recByte"   : [],
        "runtime"   : [],
        "k-1"       : [],
        "ParTime"   : []
    }
    curPath = path + "/" + speed + "-mbs"
    for p in os.listdir(curPath):
        for dataset in os.listdir(curPath + "/" + p):
            for filename in os.listdir(curPath + "/" + p + "/" + dataset):
                ppath = curPath + "/" + p + "/" + dataset
                if ".detail" not in filename :
                    continue
                method = filename[:-7]
                recByte = 0
                runtime = 0
                with open(curPath + "/" + p + "/" + dataset + "/" + filename, "r") as file:
                    pattern = r'Bytes Received:\s*(\d+)'
                    matches =  re.findall(pattern, file.read())
                    if matches:
                        for match in matches:
                            recByte += int(match)
                    else:
                        print("recByte not found")
                with open(curPath + "/" + p + "/" + dataset + "/" + filename[0:-6]+"log", "r") as file:
                    match1 = re.search(r'Finished Running engine in\s*([-+]?\d+(\.\d+)?)', file.read()).group(1)
                    runtime = float(match1)
                dic["workload"] = workload
                dic["method"].append(method)
                dic["dataset"].append(dataset)
                dic["speed"].append(speed)
                dic["p"].append(p)
                dic["recByte"].append(recByte)
                dic["runtime"].append(runtime)
                if (method,dataset,p) in check:
                    k,ParTime = check[(method,dataset,p)]
                    dic["k-1"].append(k)
                    dic["ParTime"].append(ParTime)
                else :
                    dic["k-1"].append("NULL")
                    dic["ParTime"].append("NULL")
                
    return dic

def log(content):
    import time 
    import pytz
    import datetime

    timestamp = datetime.datetime.now()
    desired_timezone = pytz.timezone('Asia/Shanghai')
    localized_time = desired_timezone.localize(timestamp)
    formatted_time = localized_time.strftime("%Y-%m-%d %H:%M:%S\t")
    
    print(formatted_time + ": " + content)

def analyzeGraph():
    curPath = "/back-up/large-cluster/comm/test_data"
    methods = ["entropy", "HYPE", "MinMax", "KaHyPar","random"]
    dic = {
        "method"    :[],
        "dataset"   :[],
        "p"         :[],
        "neigh"     :[],
        "neighTot"  :[],
        "edgeCopy"  :[],

    }
    for p in os.listdir(curPath):
        if p == "1" :
            continue
        for dataset in os.listdir(curPath + "/" + p):
            Edge = {}
            EdgeInfoPath = "/back-up/large-cluster/comm/test_data/2/"+dataset+"/edge_info.txt"
            with open(EdgeInfoPath) as file:   # e_id, v1_id, v2_id,...
                for line in file:
                    data = line[0:-1].split(" ")
                    e_id = int(data[0])
                    Edge[e_id] = [int(i) for i in data[1:]]
            for method in methods:
                log("solving " + p + " " + dataset + " " + method)
                if not os.path.exists(curPath + "/" + p + "/" + dataset + "/powergraph/" + method+"-edge.txt") :
                    # print(curPath + "/" + p + "/" + dataset + "/" + method+".txt")
                    continue
                verFile = open(curPath + "/" + p + "/" + dataset + "/" + method+".txt","r")
                edgFile = open(curPath + "/" + p + "/" + dataset + "/powergraph/" + method+"-edge.txt")
                v2p = {}
                cnt = [0 for i in range(int(p))]
                k1,k2 = 0,0 
                neighFenZi = 0
                neighFenMu = 0
                for line in verFile:
                    vid,pid = line[0:-1].split()
                    vid = int(vid)
                    v2p[vid] = int(pid)
                for eid,nodes in Edge.items():
                    pp = {}
                    for nid in nodes:
                        pid = v2p[nid]
                        if pid not in pp :
                            pp[pid] = 0
                        pp[pid] += 1
                    k1 += len(pp) - 1
                    k2 += len(pp) * (len(pp) - 1)
                    for pid in pp.keys():
                        cnt[pid] +=  1
                        neighFenZi += pp[pid] * (pp[pid] - 1)
                    neighFenMu += len(nodes) * (len(nodes) - 1)
                maxiCnt = max(cnt)
                miniCnt = min(cnt)
                # print(1.0*(maxiCnt - miniCnt)/sum(cnt)*int(p)) 
                # print(cnt)
                # print(p,method,dataset,k1,k2,maxiCnt)
                print("p:",p,"\tAlgo:",method,"\tdataset:",dataset,"\tneigh:",neighFenZi,"\tedgeCopy:",k2)
                dic["method"].append(method)
                dic["dataset"].append(dataset)
                dic["p"].append(p)
                dic["neigh"].append(neighFenZi)
                dic["neighTot"].append(neighFenMu)
                dic["edgeCopy"].append(k2)
            #     break
            # break
    return dic
                    
dic = loadPar()             
df = pd.DataFrame(data = dic)       
print(df)
df.to_csv("./parInfo.csv",index = False)          

# print(pd.DataFrame(data = loadPar()))
# dic = loadresult("/back-up/large-cluster/comm/hpagerank_result","pagerank","10")
# df = pd.DataFrame(data = dic)
# df = df[df["p"] == "8"]
# df = df[df["k-1"] != "NULL"]

# df = df[df["dataset"] == "out.dbpedia-team"]
# print(df)
# print(loadresult("/back-up/large-cluster/comm/hpagerank_result","pagerank","10"))