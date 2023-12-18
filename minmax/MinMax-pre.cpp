#include <bits/stdc++.h>
using namespace std;
void MinMax(std::string path,int n,int m,int K,int s,string output = "None"){
    FILE *file;
    file = fopen(path.c_str(),"r");
    freopen("mid-data-minmax.txt","w",stdout);

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
        nets[n_id].push_back(e_id);
    }
    cerr<<"load data ok!"<<endl;
    random_shuffle(ID.begin(), ID.end());
    for(int i=0;i<n;i++){
        printf("%d %d\n",ID[i],int(nets[ID[i]].size()));
        for(int j=0;j<nets[ID[i]].size();j++){
            if(j == 0) printf("%d",nets[ID[i]][j]);
            else printf(" %d",nets[ID[i]][j]);
        }
        printf("\n");
    }
    return;
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
    MinMax(input,n,m,p,balance,save);
}

int main(int argc,char *argv[]){
    parsingCmd(argc,argv);
}