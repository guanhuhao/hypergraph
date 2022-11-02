#include <bits/stdc++.h>
std::map<int,int> MinMax(std::string filename,int K,int s){
    std::map<int,int> n2p;
    std::vector<int> V;
    std::vector<std::set<int> > part_edge(K);
    std::vector<int> ID;

    for(int i = 0 ;i<K; i++) V.push_back(0);
    std::ifstream input;
    input.open(filename);

    int id,cnt,edge_id;
    int turn = 0;
    int pmin = 0;
    clock_t sum=0;
    int tot = 0;
    std::vector<std::vector<int> > nets;
    while(input>>id>>cnt){
        ID.push_back(id);
        nets.push_back(std::vector<int>());
        for(int i=0;i<cnt;i++) {
            input>>edge_id;
            nets[tot].push_back(edge_id);
        }
        tot++;
    }
    clock_t beg = std::clock();
    while(turn<tot){
        int id = ID[turn];
        // if(turn%100 == 0){
        //     std::cerr<<"turn:"<<turn<<std::endl;
        // }
        
        int saved = -1;
        int p = 0;
        for(int i=0;i<K;i++){
            if(V[i]-V[pmin] > s) continue;
            int cnt = 0;
            for(auto &x:nets[turn]){
                if(part_edge[i].find(x)!=part_edge[i].end()) {
                    cnt++;
                }
            }
            if(cnt>=saved){
                saved = cnt;
                p = i;
            }
        }
        for(auto &x:nets[turn]) part_edge[p].insert(x);
        
        V[p]++;
        n2p[id] = p;
        if(p == pmin){
            for(int i=0;i<K;i++){
                if(V[i]<V[pmin]) pmin = i;
            }
        }
        turn ++;
    }
    clock_t end = std::clock();
    std::cerr<<"runtime:"<<(end-beg)*1000/CLOCKS_PER_SEC<<std::endl;   
    for(int i=0;i<K;i++){
        std::cerr<<"par:"<<i<<" size:"<<V[i]<<" edge:"<<part_edge[i].size()<<std::endl;
    }
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
int main(){
    std::ios::sync_with_stdio(false);
    std::map<int,int> n2p;
    // std::map<int,std::vector<int> > e2n;
    // std::string filename = "../data/github/vertex_stream.txt";
    std::string filename = "../data/github/vertex_stream.txt";

    clock_t beg = std::clock();
    n2p = MinMax(filename,10,100);
    clock_t end = std::clock();

    std::map<int,std::vector<int> > e2n = E2N(filename);
    int k = 0;
    for(auto &x:e2n){
        int edge_id = x.first;
        std::vector<int> vertex = x.second;
        std::set<int> st;
        for(auto &v:vertex){
            st.insert(n2p[v]);
        }
        k += st.size()-1; 

    }
    std::cerr<<"k-1:"<<k<<std::endl;
}