#include <bits/stdc++.h>
#include "data.h"
// #include "partition.hpp"
using namespace std;
int n,m;
HyperNode *Node;
HyperEdge *Edge;
class Score_List{
public:
    int maxi_degree;
    int num_node;
    int cur_maxi;
    // HyperNode *Node;
    // HyperEdge *Edge;
    vector<unordered_map<int,int> > degree_set;
    unordered_map<int,int> Eval;
    unordered_map<int,bool> assign;
    Score_List(int Maxi_degree,int Num_node){
        cur_maxi = 0;
        this->maxi_degree = Maxi_degree;
        this->num_node = Num_node;
        for(int i=0; i<=Maxi_degree;i++){
            degree_set.push_back(unordered_map<int,int>());
            // cerr<<"begin "<<i<<" "<<degree_set[i].size()<<endl;
        }
        for(int i=0;i<num_node;i++) degree_set[0][i] = 1;
    }
    void add(int id){
        if(assign[id] == true) return;
        int pre_v = Eval[id];
        Eval[id] ++;
        int aft_v = Eval[id];

        degree_set[pre_v].erase(id);
        degree_set[aft_v][id] = 1;
        // cerr<<"add size:"<<degree_set[cur_maxi].size()<<endl;
        if(aft_v>cur_maxi) cur_maxi = aft_v;
    }
    int top(){
        // cerr<<"size:"<<degree_set[cur_maxi].size()<<" "<<<<endl;
        assert(degree_set[cur_maxi].size() != 0);
        for(auto &item : degree_set[cur_maxi])  {
            assert(assign[item.first] == false);
            return item.first; 
        }
        return -1;
    }
    void erase(int id){
        // cerr<<"ass:"<<assign[id]<<endl;
        assert(assign[id] == false);
        assign[id] = true;
        degree_set[Eval[id]].erase(id);
        if(Eval[id] == cur_maxi) {
            while(degree_set[cur_maxi].size() == 0) cur_maxi --;
        }
    }
    void clear(){
        cur_maxi = 0;
        Eval = unordered_map<int,int>();
        for(int i=0; i<=maxi_degree;i++) degree_set[i].clear();
        
        for(int i=0;i<num_node;i++) {
            if(assign[i] == true) continue;
            degree_set[0][i] = 1;
        }
    }
};
void load_data(string path,HyperNode * Node,HyperEdge * Edge){
    unordered_map<int,HyperNode> mp_node;
    FILE *file;
    file = fopen(path.c_str(),"r");
    int n_id,e_id;
    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        Node[n_id].degree += 1;
        Edge[e_id].degree += 1;
        Node[n_id].edges.push_back(e_id);
        Edge[e_id].nodes.push_back(n_id);
    }
}

void solve(int n,int m, HyperNode *Node, HyperEdge *Edge, int p, int shield_heavy_node = 1e9){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // topk: add topk node at once 
    // buffer_fac: set buffer to reduce search range 
    // shield_heavy_node: shield heavy node to speed and improve quality

    int maxi_cap = n/p + 1;
    vector<unordered_map<int,int> > part_node;
    vector<unordered_map<int,int> > part_edge;
    int maxi_degree = 0;
    for(int i = 0; i<n; i++) maxi_degree = max(Node[i].degree,maxi_degree);
    Score_List score_list(maxi_degree,n);

    int cnt = 0;
    int cur_p = 0;
    part_node.push_back(unordered_map<int,int>());
    part_edge.push_back(unordered_map<int,int>());
    clock_t beg_time = clock();
    int cnt_big = 0;
    vector<int> node_list;
    for(int i=0;i<n;i++) node_list.push_back(i);
    while(cnt < n){     
        cnt += 1; 
        // cerr<<"turn:"<<cnt<<endl;
        clock_t beg;
        int add_node = score_list.top();
        score_list.erase(add_node);

        part_node[cur_p][add_node] = 1;
        for(auto &e_id:Node[add_node].edges){
            if(part_edge[cur_p][e_id] == 0){
                part_edge[cur_p][e_id] = 1;
                if(Edge[e_id].degree > shield_heavy_node) continue;
                for(auto &n_id:Edge[e_id].nodes){
                    score_list.add(n_id);
                }
            }
        }
 
        if(part_node[cur_p].size() >= maxi_cap){
            cur_p += 1;
            score_list.clear();
            part_node.push_back(unordered_map<int,int>());
            part_edge.push_back(unordered_map<int,int>());      
        }
    }
    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<part_edge.size();i++) {
        // cerr<<"i:"<<i<<" "<<part_edge[i].size()<<endl;
        k_1 += part_edge[i].size();
        for(auto &e_id:part_edge[i]) edge_set.insert(e_id.first);
    }
    cerr<<"cnt_big:"<<cnt_big<<endl;
    cerr<<"parameter:"<<endl<<"p:"<<p<<" shield_heavy_node:"<<shield_heavy_node<<endl;
    cerr<<"k-1: "<<k_1-edge_set.size()<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
}
int main(){
    // n = 4600;
    // m = 4600;
    // string path = "../data/wiki/wiki.txt";

    n = 56520;
    m = 120870;
    string path = "../data/github/github.txt";

    Node = new HyperNode[n];
    Edge = new HyperEdge[m];
    for(int i=0;i<n;i++) Node[i].id = i;
    for(int i=0;i<m;i++) Edge[i].id = i;
    // load_data(path,Node,Edge);
    load_data(path,Node,Edge);
    for(int i=2; i<10; i++){
        int p = 16;
        int shield_heavy_node = 10*i;
        solve(n,m,Node,Edge,p,shield_heavy_node);
    }

    return 0;
}
