#include <bits/stdc++.h>
using namespace std;
std::map<int,int> MinMax(std::string path,int n,int m,int K,int s,string output = "None"){
    FILE *file;
    file = fopen(path.c_str(),"r");

    FILE *result;
    if(output != "None") {
        result = fopen(output.c_str(),"w");
    }

    std::map<int,int> n2p;
    std::vector<int> V;
    std::vector<std::set<int> > part_edge(K);
    std::vector<int> ID;

    for(int i = 0 ;i<K; i++) V.push_back(0);
    clock_t beg = std::clock();
    int n_id,e_id;
    int turn = 0;
    int pmin = 0;
    clock_t sum=0;
    int tot = 0;
    std::vector<std::vector<int> > nets(n+1);

    for(int i=1;i<=n;i++) {
        ID.push_back(i); 
        nets.push_back(std::vector<int>());
    }
    tot = n;

    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        assert(n_id<=n);
        // cerr<<n_id<<" "<<e_id<<endl;
        nets[n_id].push_back(e_id);
    }
    cerr<<"load data ok!"<<endl;
    random_shuffle(ID.begin(), ID.end());
    while(turn<tot){
        int n_id = ID[turn];
        
        int saved = -1;
        int p = 0;
        for(int i=0;i<K;i++){
            if(V[i]-V[pmin] > s) continue;
            int cnt = 0;
            for(auto &x:nets[n_id]){
                if(part_edge[i].find(x)!=part_edge[i].end()) {
                    cnt++;
                }
            }
            if(cnt>=saved){
                saved = cnt;
                p = i;
            }
        }
        for(auto &x:nets[n_id]) part_edge[p].insert(x);
        // cerr<<2<<endl;
        V[p]++;
        // cerr<<output<<endl;
        if(output != "None"){
            fprintf(result,"%d %d\n",n_id,p); 
        }
        n2p[n_id] = p;
        // cerr<<3<<endl;
        if(p == pmin){
            for(int i=0;i<K;i++){
                if(V[i]<V[pmin]) pmin = i;
            }
        }
        turn ++;
    }
    clock_t end = std::clock();
    std::cerr<<"runtime:"<<(end-beg)*1000/CLOCKS_PER_SEC<<std::endl;   
    clock_t tot_time = (end-beg)*1000/CLOCKS_PER_SEC;
    int k_1 = 0;
    for(int i=0;i<K;i++){
        // std::cerr<<"par:"<<i<<" size:"<<V[i]<<" edge:"<<part_edge[i].size()<<std::endl;
        k_1 += part_edge[i].size();
    }
    if(K == 2) {
        cout<<"\n# MIN-MAX  - dataset:"<<filename<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 ,  total time "<<endl; 
    }
    cout<<K<<","<<k_1-m<<", ,"<<tot_time<<endl;
    // cout<<endl;
    return n2p;
}

std::map<int,std::vector<int> > E2N(std::string filename){
    std::map<int,std::vector<int> > e2n;

    std::ifstream input;
    input.open(filename);

    int id,cnt,edge_id;
    while(input >> id >> cnt){
        std::set<int> nets;
        for(int i=0;i<cnt;i++) {
            input>>edge_id;
            if(e2n.find(edge_id) == e2n.end()){
                e2n[edge_id] = std::vector<int>();
            }
            e2n[edge_id].push_back(id);
        }
    }
    return e2n;

}
vector<int> nn,mm;
vector<string> filename;

void parsingCmd(int argc,char *argv[]){
    string input="../data/out.github";
    int n = 56530;
    int m = 120869;
    int p = 16;
    double balance = 0.05;
    string result_path = "./minmax-result.txt";
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
        }else if(std::string(argv[i]) == "-o" && i + 1 < argc){
            result_path = argv[i + 1];
        }else if(std::string(argv[i]) == "-save" && i + 1 < argc){
            save = argv[i + 1];
        }
    }

    freopen(result_path.c_str(),"w",stdout);
    cout<<"parameters:"<<endl;
    cout<<"dataset:"<<input<<"\tn:"<<n<<"\tm:"<<m<<endl;
    cout<<"p:"<<p<<"\tbalance:"<<balance<<endl;
    cout<<"logFile:"<<result_path<<endl;
    cout<<"save partitionFile:"<<save<<endl;
    MinMax(input,n,m,p,balance,save);
}

int main(int argc,char *argv[]){
    parsingCmd(argc,argv);
}