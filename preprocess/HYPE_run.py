import os 
import re

data_path = os.getcwd()+"/../data/"
os.system("rm "+data_path+"*partition*")
for file in os.listdir(data_path):
    if re.match("(.*)ipynb(.*)",file) != None : continue
    if os.path.isdir(data_path+file) == True : continue
    if re.match("(.*)orkut(.*)",file) != None : continue
    if re.match("(.*)tracker(.*)",file) != None : continue
    if re.match("(.*)rand(.*)",file) != None : continue
    
    print("solving ",file)
    
    p = 1
    while(p<64):
        p *= 2
        out_path = "../simulation/test_data/"+str(p)+"/"+file+"/HYPE.txt"
#         if os.path.exists(out_path) : continue
            
        os.system("rm "+data_path+"*partition*")
        cmd = "stdbuf -o0 ./HYPE -f bipartite -i "+ data_path +file +" -p " + str(p) + " -o" +" 1>./out.log"
        os.system(cmd)
        result_file = open(out_path,"w")
        result_file.close()
        print("out file:"+out_path)
        
        result_file = open(out_path,"a")
        for outfile in os.listdir(data_path):
            if re.match("(.*)_partition_(.*)",outfile) == None : continue
                    
            name = re.match("(.*)_partition_(.*)",outfile)[1]
            p_id = re.match("(.*)_partition_(.*)",outfile)[2]

            print("solving ",name," ",p_id)
            with open(data_path+"/"+outfile,"r") as f:
                cnt = 0
                for line in f:
                    cnt += 1
                    if cnt <= 2 : continue
        #             print(line[0:-1]+" "+str(p_id))
        #             result_file.write(str(p_id)+"\n")
                    result_file.write(line[0:-1]+" "+str(p_id)+"\n")
        #             print("ok")
        #             break
        result_file.close()
    