import os 
import re

data_path = os.getcwd()+"/../data/"
# os.system("rm "+data_path+"*partition*")
for file in os.listdir(data_path):
    # if re.match("(.*)wiki(.*)",file) == None : continue
    if re.match("(.*)ipynb(.*)",file) != None : continue
    if os.path.isdir(data_path+file) == True : continue
    if re.match("(.*)orkut(.*)",file) != None : continue
    if re.match("(.*)tracker(.*)",file) != None : continue
    if re.match("(.*)rand(.*)",file) != None : continue
    if re.match("(.*)author(.*)",file) != None : continue
    
    print("solving ",file)


    edges = {}
    dic_n = set()
    dic_e = set()
    print("format trans...")
    with open(data_path +file,"r") as f:
        for line in f:
            u,v = re.split(" |\t",line[0:-1])[0:2]
            u = int(u)
            v = int(v)

            dic_n.add(u)
            dic_e.add(v)

            if edges.get(v) == None : edges[v] = []
            edges[v].append(u)
    print("generating data file...")
            
    with open("./KaHypar-mid-data","w") as f:
        f.write(str(max(dic_e))+" "+str(max(dic_n))+"\n")
        for i in range(max(dic_e)):
            if edges.get(i) == None : edges[i] = [1]
#             print(i)
#             print(nodes[i])
            # if edges.get(i) == None : 
            #     # print(123)
            #     f.write("1\n")
            #     continue
            for j in range(len(edges[i])):
                if j!=0: f.write(" "+str(edges[i][j]))
                else : f.write(str(edges[i][j]))
            f.write("\n")
    print("datafile ok!")
    
    p = 1
    while(p<64):
        p *= 2
        out_path = "../simulation/test_data/"+str(p)+"/"+file+"/KaHypar.txt"
#         if os.path.exists(out_path) : continue
            
        # os.system("rm "+data_path+"*partition*")
        cmd = "stdbuf -o0 ./KaHyPar -h ./KaHypar-mid-data -k " + str(p) +" -e 0.03 -o km1 -m direct -p ./config/km1_kKaHyPar_sea20.ini -w true  1>./KaHypar.log"
        print("cmd:",cmd)
        # cmd = "stdbuf -o0 ./HYPE -f bipartite -i "+ data_path +file +" -p " + str(p) + " -o" +" 1>./out.log"
        os.system(cmd)
        result_file = open(out_path,"w")
        result_file.close()
        print("out file:"+out_path)
        
        result_file = open(out_path,"a")
        with open("KaHypar-mid-data.part"+str(p)+".epsilon0.03.seed-1.KaHyPar","r") as f:
            ll = 1
            for line in f: 
                par = int(line)
                result_file.write(str(ll)+" "+str(par)+"\n")
                ll += 1

        # for outfile in os.listdir(data_path):
        #     if re.match("(.*)_partition_(.*)",outfile) == None : continue
                    
        #     name = re.match("(.*)_partition_(.*)",outfile)[1]
        #     p_id = re.match("(.*)_partition_(.*)",outfile)[2]

        #     print("solving ",name," ",p_id)
        #     with open(data_path+"/"+outfile,"r") as f:
        #         cnt = 0
        #         for line in f:
        #             cnt += 1
        #             if cnt <= 2 : continue
        # #             print(line[0:-1]+" "+str(p_id))
        # #             result_file.write(str(p_id)+"\n")
        #             result_file.write(line[0:-1]+" "+str(p_id)+"\n")
        # #             print("ok")
        # #             break
        # result_file.close()
        # break
    
os.system("rm *KaHypar-mid-data*")