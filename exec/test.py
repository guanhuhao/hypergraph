scheme_path = "/raid/guan/large-cluster/comm/test_data/2/out.dblp-author/KaHyPar.txt" # generate partition scheme
result_file = open(scheme_path,"w")
result_file.close()

result_file = open(scheme_path,"a")
with open("KaHyPar-mid-data.part2.epsilon0.03.seed-1.KaHyPar","r") as f:
    ll = 1
    for line in f: 
        par = int(line)
        result_file.write(str(ll)+" "+str(par)+"\n")
        ll += 1