#include <bits/stdc++.h>
std::map<int,int> MinMax(std::string filename,int K,int s){
    std::map<int,int> n2p;
    std::vector<std::set<int> > V(K);
    std::vector<std::set<int> > part_edge(K);
    for(int i = 0 ;i<K;i++) {
        // V.push_back(std::set<int>());
        // part_edge.push_back(std::set<int>());
    }
    std::ifstream input;
    input.open(filename);

    int id,cnt,edge_id;
    int turn = 0;
    int pmin = 0;
    while(input >> id >> cnt){
        turn ++;
        // if(turn%100 == 0){
        //     std::cerr<<"turn:"<<turn<<std::endl;
        // }
        std::set<int> nets;
        for(int i=0;i<cnt;i++) {
            input>>edge_id;
            nets.insert(edge_id);
        }
        int saved = -1;
        int p = 0;
        std::vector<int> add;
        for(int i=0;i<K;i++){
            if(V[i].size()-V[pmin].size() > s) continue;
            std::set<int>* a;
            std::set<int>* b;
            
            a = &nets;
            b = &part_edge[i];
            // if(a->size()>b->size()) swap(a,b);
            int cnt = 0;
            for(auto &x:*a){
                if(b->find(x)!=b->end()) {
                    cnt++;
                }
            }
            if(cnt>saved){
                add.clear();
                saved = cnt;
                p = i;
                for(auto &x:*a){
                    if(b->find(x) == b->end()) add.push_back(x);
                }
            }
        }
        // std::cerr<<"select:"<<p<<" "<<V[p].size()<<std::endl;
        for(auto &x:add) part_edge[p].insert(x);
        
        // std::set_union(nets.begin(),nets.end(),part_edge[p].begin(),part_edge[p].end(), std::inserter(part_edge[p],part_edge[p].begin()));
        // for(auto &x:add){}
        V[p].insert(id);
        n2p[id] = p;
        if(p == pmin){
            for(int i=0;i<K;i++){
                if(V[i].size()<V[pmin].size()) pmin = i;
            }
        }

    }
    for(int i=0;i<K;i++){
        std::cerr<<"par:"<<i<<" size:"<<V[i].size()<<std::endl;
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
    std::map<int,std::vector<int> > e2n;
    std::string filename = "../data/github/vertex_stream.txt";
    clock_t beg = std::clock();
    n2p = MinMax(filename,16,100);
    e2n = E2N(filename);
    clock_t end = std::clock();
    std::cerr<<"runtime:"<<(end-beg)*1000/CLOCKS_PER_SEC<<std::endl;

    int k = 0;
    for(auto &x:e2n){
        int edge_id = x.first;
        std::vector<int> vertex = x.second;
        std::set<int> st;
        for(auto &v:vertex){
            st.insert(n2p[v]);
        }
        // std::cerr<<st.size()<<std::endl;
        k += st.size()-1; 

    }
    std::cerr<<"k-1:"<<k<<std::endl;
}