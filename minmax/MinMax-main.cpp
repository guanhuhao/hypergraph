#include <bits/stdc++.h>
using namespace std;
void MinMax(std::string path,int n,int m,int K,int s,string output = "None"){
    std::vector<int> V;
    std::vector<std::set<int> > part_edge(K);
    int pmin = 0;
    int turn = 0;
    FILE *result;
    if(output != "None") {
        result = fopen(output.c_str(),"w");
    }
    for(int i = 0 ;i<K; i++) V.push_back(0);
    clock_t beg = std::clock();

    while(turn<n){
        // cout<<turn<<endl;
        int nid, num;
        scanf("%d%d",&nid,&num);
        vector<int> edges(num);
        for(int i=0;i<num;i++) scanf("%d",&edges[i]);
        
        
        int saved = -1;
        int p = 0;
        for(int i=0;i<K;i++){
            if(V[i]-V[pmin] > s) continue;
            int cnt = 0;
            for(auto &x:edges){
                if(part_edge[i].find(x)!=part_edge[i].end()) {
                    cnt++;
                }
            }
            if(cnt>=saved){
                saved = cnt;
                p = i;
            }
        }
        for(auto &x:edges) part_edge[p].insert(x);
        // cerr<<2<<endl;
        V[p]++;
        // cerr<<output<<endl;
        if(output != "None"){
            fprintf(result,"%d %d\n",nid,p); 
        }
        // cerr<<3<<endl;
        if(p == pmin){
            for(int i=0;i<K;i++){
                if(V[i]<V[pmin]) pmin = i;
            }
        }
        turn ++;
    }
    clock_t end = std::clock();
    clock_t tot_time = (end-beg)*1000/CLOCKS_PER_SEC;
    int k_1 = 0;
    for(int i=0;i<K;i++){
        k_1 += part_edge[i].size();
    }
    cout<<"k-1: "<<k_1-m<<endl;
    cout<<"runtime: "<<tot_time<<endl;
    return;
}


void parsingCmd(int argc,char *argv[]){
    string input="../data/out.github";
    int n = 56530;
    int m = 120869;
    int p = 16;
    double balance = 0.05;
    string save = "None";

    for (int i = 1; i < argc; ++i) {
        // 检查是否有 -o 选项
        if (std::string(argv[i]) == "-i" && i + 1 < argc) {
            input = argv[i + 1];
        }else if(std::string(argv[i]) == "-n" && i + 1 < argc){
            n = stoi(argv[i + 1]);
        }else if(std::string(argv[i]) == "-m" && i + 1 < argc){
            m = stoi(argv[i + 1]);
        }else if(std::string(argv[i]) == "-p" && i + 1 < argc){
            p = stoi(argv[i + 1]);
        }else if(std::string(argv[i]) == "-balance" && i + 1 < argc){
            balance = strtod(argv[i + 1], NULL);
        }else if(std::string(argv[i]) == "-save" && i + 1 < argc){
            save = argv[i + 1];
        }
    }

    cout<<"parameters:"<<endl;
    cout<<"dataset:"<<input<<"\tn:"<<n<<"\tm:"<<m<<endl;
    cout<<"p:"<<p<<"\tbalance:"<<balance<<endl;
    cout<<"save partitionFile:"<<save<<endl;

    freopen("mid-data-minmax.txt","r",stdin);
    MinMax(input,n,m,p,balance,save);
}

int main(int argc,char *argv[]){
    parsingCmd(argc,argv);
}