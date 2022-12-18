#include <bits/stdc++.h>
#include "data.hpp"
// #include "partition.hpp"
using namespace std;
int n,m;
HyperNode *Node;
HyperEdge *Edge;
typedef pair<int,int> P;
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
        if(aft_v>cur_maxi) cur_maxi = aft_v;
    }
    int top(){
        if(degree_set[cur_maxi].size() == 0) return -1;
        for(auto &item : degree_set[cur_maxi])  {
            assert(assign[item.first] == false);
            return item.first; 
        }
        return -1;
    }
    void erase(int id){
        assert(assign[id] == false);
        assign[id] = true;
        degree_set[Eval[id]].erase(id);
        if(Eval[id] == cur_maxi) {
            while(cur_maxi != 0 && degree_set[cur_maxi].size() == 0) cur_maxi --;
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
    int turn = 0;
    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        assert(n_id<n);
        assert(e_id<m);
        Node[n_id].degree += 1;
        Edge[e_id].degree += 1;
        Node[n_id].edges.push_back(e_id);
        Edge[e_id].nodes.push_back(n_id);
    }
}

void solve(int n,int m, HyperNode *Node, HyperEdge *Edge, int p, int shield_heavy_node = 1e9,double prob = 0){
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
    vector<P> degree_list;
    for(int i = 0; i<n; i++) {
        maxi_degree = max(Node[i].degree,maxi_degree);
        degree_list.push_back(P(Node[i].degree,i));
    }
    sort(degree_list.begin(),degree_list.end(),greater<P>());
    Score_List score_list(maxi_degree,n);
    vector<int> wait_assign;
    int cnt = 0;
    int cur_p = 0;
    for(int i=0;i<n*prob;i++){
        wait_assign.push_back(degree_list[i].second);
        score_list.erase(degree_list[i].second);
    }
    part_node.push_back(unordered_map<int,int>());
    part_edge.push_back(unordered_map<int,int>());    
    clock_t time1 = clock();
    clock_t beg_time = clock();
    int cnt_big = 0;

    int cnt_add = 0;
    while(cnt < n){   
        cnt ++; 
        int add_node = score_list.top();
        if(add_node == -1){
            add_node = wait_assign.back();
            wait_assign.pop_back();
            part_node[cur_p][add_node] = 1;
            for(auto &e_id:Node[add_node].edges) part_edge[cur_p][e_id] = 1;
        }
        else {
            score_list.erase(add_node);
            part_node[cur_p][add_node] = 1;
            for(auto &e_id:Node[add_node].edges){
                part_edge[cur_p][e_id] += 1;
                Edge[e_id].erase(add_node);
                if(part_edge[cur_p][e_id] == 1){
                    if(Edge[e_id].degree > shield_heavy_node) continue;
                    // for(auto &item:Edge[e_id].nodes){
                    //     int n_id = item;
                    //     score_list.add(n_id);
                    //     cnt_add += 1; 
                    // }
                    for(auto &item:Edge[e_id].rest){
                        int n_id = item.first;
                        score_list.add(n_id);
                        cnt_add += 1; 
                    }
                }
            }
        }
 
        if(part_node[cur_p].size() >= maxi_cap){
            cnt_add = 0;
            // cerr<<cur_p<<": "<<"time:"<<(clock()-time1)*1000/CLOCKS_PER_SEC<< " edge num:"<<part_edge[cur_p].size()<<" node num:"<<part_node[cur_p].size()<<endl;
            time1 = clock();
            cur_p += 1;
            score_list.clear();
            part_node.push_back(unordered_map<int,int>());
            part_edge.push_back(unordered_map<int,int>());      
        }
    }
    // cerr<<cur_p<<": "<<"time:"<<(clock()-time1)*1000/CLOCKS_PER_SEC<< " edge num:"<<part_edge[cur_p].size()<<" node num:"<<part_node[cur_p].size()<<endl;

    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<p;i++) {
        k_1 += part_edge[i].size();
        double ave = 0;
        for(auto &item:part_edge[i]){
            int e_id = item.first;
            ave += 1.0*part_edge[i][e_id]/Edge[e_id].degree;
        }
        ave /= part_edge[i].size();
        // cerr<<i<<": "<<" edge num:"<<part_edge[i].size()<<" node num:"<<part_node[i].size()<<" ave:"<<ave<<endl;
    }
    cerr<<"cnt_big:"<<cnt_big<<endl;
    cerr<<"parameter:"<<endl<<"p:"<<p<<" shield_heavy_node:"<<shield_heavy_node<<endl;
    cerr<<"k-1: "<<k_1-m<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
}
int main(){
    // n = 4600;
    // m = 4600;
    // string path = "../data/wiki/wiki.txt";

    // n = 56520;
    // m = 120870;
    // string path = "../data/github/github.txt";

    // n = 901167;
    // m = 34462;
    // string path = "../data/dbpedia-team/out.dbpedia-team";

    n = 127824;
    m = 383641;
    string path = "../data/actor-movie/out.actor-movie";

    // n = 172080;
    // m = 53408;
    // string path = "../data/dbpedia-location/out.dbpedia-location";
    
    // n = 1953086;
    // m = 5624220;
    // string path = "../data/dblp-author/out.dblp-author";


    Node = new HyperNode[n];
    Edge = new HyperEdge[m];
    for(int i=0;i<n;i++) Node[i].id = i; 
    for(int i=0;i<m;i++) Edge[i].id = i;
    cerr<<"begin load data!"<<endl;
    load_data(path,Node,Edge);
    cerr<<"load data OK!"<<endl;

    for(int i=60; i<=80; i++){
        int p = 64;
        int shield_heavy_node = i;
        // double prob = 1.0/p;
        double prob = 0;
        for(int j=0;j<m;j++) Edge[j].reset();
        solve(n,m,Node,Edge,p,shield_heavy_node,prob);
    }
    //}

    return 0;
}
