#include <bits/stdc++.h>
using namespace std;
std::map<int,int> MinMax(std::string path,int n,int m,int K,int s,string output = "None"){
    FILE *file;
    file = fopen(path.c_str(),"r");

    string result_path = path;
    string filename;
    while (result_path.back()!='/') {
        filename.push_back(result_path.back());
        result_path.pop_back();
    }
    reverse(filename.begin(),filename.end());
    result_path = result_path+"MinMax-par/"+filename;
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
        
        V[p]++;
        if(output != "None"){
            fprintf(result,"%d %d\n",n_id,p); 
            // for(auto &e_id:nets[n_id]){
            // fprintf(result,"%d %d %d\n",n_id,p);
            // // fprintf(result,"%d %d %d\n",e_id+n,n_id,p);
            // }
        }
        n2p[n_id] = p;
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
        std::cerr<<"par:"<<i<<" size:"<<V[i]<<" edge:"<<part_edge[i].size()<<std::endl;
        k_1 += part_edge[i].size();
    }
    if(K == 2) {
        cout<<"# MIN-MAX  - dataset:"<<filename<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 ,  total time "<<endl; 
    }
    cout<<K<<","<<k_1-m<<","<<tot_time<<endl;
    cout<<endl;
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
void init_data(){
    nn.push_back( 127823 );
    mm.push_back( 383640 );
    filename.push_back( "../data/out.actor-movie" );

    nn.push_back( 383640 );
    mm.push_back( 127823 );
    filename.push_back( "../data/out.actor-movie-swap.txt" );

    nn.push_back( 1953085 );
    mm.push_back( 5624219 );
    filename.push_back( "../data/out.dblp-author" );

    nn.push_back( 5623931 );
    mm.push_back( 1953085 );
    filename.push_back( "../data/out.dblp-author-swap.txt" );

    nn.push_back( 172091 );
    mm.push_back( 53407 );
    filename.push_back( "../data/out.dbpedia-location" );

    nn.push_back( 53407 );
    mm.push_back( 172091 );
    filename.push_back( "../data/out.dbpedia-location-swap.txt" );

    nn.push_back( 901166 );
    mm.push_back( 34461 );
    filename.push_back( "../data/out.dbpedia-team" );

    nn.push_back( 34461 );
    mm.push_back( 901166 );
    filename.push_back( "../data/out.dbpedia-team-swap.txt" );

    nn.push_back( 56519 );
    mm.push_back( 120867 );
    filename.push_back( "../data/out.github" );

    nn.push_back( 120867 );
    mm.push_back( 56519 );
    filename.push_back( "../data/out.github-swap.txt" );

    // nn.push_back( 2783196 );
    // mm.push_back( 8730857 );
    // filename.push_back( "../data/out.orkut-groupmemberships" );

    // nn.push_back( 8730857 );
    // mm.push_back( 2783196 );
    // filename.push_back( "../data/out.orkut-groupmemberships-swap.txt" );

    // nn.push_back( 27665730 );
    // mm.push_back( 12756244 );
    // filename.push_back( "../data/out.trackers" );

    // nn.push_back( 12756244 );
    // mm.push_back( 27665730 );
    // filename.push_back( "../data/out.trackers-swap.txt" );

    nn.push_back( 4566 );
    mm.push_back( 4131 );
    filename.push_back( "../data/wiki_new.txt" );

    nn.push_back( 4131 );
    mm.push_back( 4566 );
    filename.push_back( "../data/wiki_new.txt-swap.txt" );

    // nn.push_back( 10000000 );
    // mm.push_back( 10000000 );
    // filename.push_back( "../data/rand-n10M-m10M-e100M" );
}
void unit_test(){ // diffrent dataset and p
    init_data();
    freopen("./MIN-MAX_result.txt","w",stdout);
    for(int i=0;i<nn.size();i++){
        cerr<<"begin solve "<<filename[i]<<endl;
        int n = nn[i];
        int m = mm[i];
        string f = filename[i];
        for(int j=2;j<=64;j*=2){
            MinMax(f,n,m,j,int(n*0.01/j));
            cerr<<j<<" ok!"<<endl;
            cerr<<"------------"<<endl;
        } 
    }
}
void unit_test2(){ // generate par result
    init_data();
    freopen("./MIN-MAX_result.txt","w",stdout);
    for(int p =2;p<=64;p*=2){
        for(int i=0;i<nn.size();i++){
            cerr<<"begin solve "<<filename[i]<<endl;
            int n = nn[i];
            int m = mm[i];
            string f = filename[i];
            // int p = 16;

            string result_path = f;
            string filename;
            while (result_path.back()!='/') {
                filename.push_back(result_path.back());
                result_path.pop_back();
            }
            reverse(filename.begin(),filename.end());
            result_path = "../simulation/test_data/"+to_string(p)+"/"+filename+"/MinMax.txt";

            MinMax(f,n,m,p,int(n*0.01),result_path);
            cerr<<"------------"<<endl;
        }
    }
}
int main(){
    unit_test2();
}