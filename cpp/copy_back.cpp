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
    vector<unordered_set<int> > degree_set;
    unordered_map<int,int> Eval;
    unordered_map<int,bool> assign;
    Score_List(int Maxi_degree,int Num_node){
        cur_maxi = 0;
        this->maxi_degree = Maxi_degree;
        this->num_node = Num_node;
        for(int i=0; i<=Maxi_degree;i++){
            degree_set.push_back(unordered_set<int>());
        }
        for(int i=0;i<num_node;i++) degree_set[0].insert(i);
    }
    void add(int id){
        if(assign[id] == true) return;
        int pre_v = Eval[id];
        Eval[id] ++;
        int aft_v = Eval[id];

        degree_set[pre_v].erase(id);
        degree_set[aft_v].insert(id);
        if(aft_v>cur_maxi) cur_maxi = aft_v;
    }

    void sub(int id,int val=1){
        if(assign[id] == true) return;
        int pre_v = Eval[id];
        Eval[id] -=val;
        int aft_v = Eval[id];
        degree_set[pre_v].erase(id);
        degree_set[aft_v].insert(id);
        while(cur_maxi != 0 && degree_set[cur_maxi].size() == 0) cur_maxi --;
    }
    
    int top(){
        if(degree_set[cur_maxi].size() == 0) return -1;
        for(auto &n_id : degree_set[cur_maxi])  {
            assert(assign[n_id] == false);
            return n_id; 
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
        Eval = unordered_map<int,int>();
        cur_maxi = 0;
        for(int i=0; i<=maxi_degree;i++) degree_set[i].clear();
        
        for(int i=0;i<num_node;i++) {
            if(assign[i] == true) continue;
            degree_set[0].insert(i);
        }
    }
};
void load_data(string path,HyperNode * Node,HyperEdge * Edge){
    FILE *file;
    file = fopen(path.c_str(),"r");
    int n_id,e_id;
    int turn = 0;
    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        assert(n_id<n);
        assert(e_id<m);
        Node[n_id].degree += 1;
        Edge[e_id].degree += 1;
        Node[n_id].edges.insert(e_id);
        Edge[e_id].nodes.insert(n_id);
    }
}

void solve(int n,int m, HyperNode *Node, HyperEdge *Edge, int p, int shield_heavy_node = 1e9,double prob = 0, double fac=0){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // topk: add topk node at once 
    // buffer_fac: set buffer to reduce search range 
    // shield_heavy_node: shield heavy node to speed and improve quality

    int maxi_cap = n/p + 1;
    vector<unordered_set<int> > part_node;
    vector<unordered_map<int,int> > part_edge;
    int maxi_degree = 0;
    vector<P> degree_list;
    double tot_deg = 0;
    for(int i = 0; i<n; i++) {
        maxi_degree = max(Node[i].degree,maxi_degree);
        degree_list.push_back(P(Node[i].degree,i));
        tot_deg += Node[i].degree;
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
    part_node.push_back(unordered_set<int>());
    part_edge.push_back(unordered_map<int,int>());    
    clock_t time1 = 0;
    clock_t time2 = 0;
    clock_t beg_time = clock();
    clock_t beg_t;
    int cnt_big = 0;

    int cur_deg = tot_deg;
    unordered_set<int> check_edge;
    while(cnt < n){   
        cnt ++; 
        int add_node = score_list.top();
        if(add_node == -1){
            add_node = wait_assign.back();
            wait_assign.pop_back();
            part_node[cur_p].insert(add_node);
            for(auto &e_id:Node[add_node].edges) part_edge[cur_p][e_id] = 1;
        }
        else {
            beg_t = clock();
            score_list.erase(add_node);
            part_node[cur_p].insert(add_node);
            for(auto &e_id:Node[add_node].edges){
                part_edge[cur_p][e_id] += 1;
                // Edge[e_id].erase(add_node);
                if(check_edge.find(e_id) != check_edge.end()) continue;
                if(part_edge[cur_p][e_id] == 1){
                    // double rest_per = 1.0*Edge[e_id].rest/Edge[e_id].degree;
                    // double ave_per = 1.0*cur_deg/tot_deg;
                    // if(rest_per < ave_per*fac ) continue;
                    if(Edge[e_id].degree > shield_heavy_node) continue;
                    check_edge.insert(e_id);
                    for(auto &n_id:Edge[e_id].nodes){score_list.add(n_id);}
                }
                Edge[e_id].rest--;
                cur_deg--;
            }
            time1 += (clock()-beg_t)*1000/CLOCKS_PER_SEC;
        }
 
        if(part_node[cur_p].size() >= maxi_cap){
            beg_t = clock();
            // vector<pair<double,int> > edge_v;
            // for(auto &item:part_edge[cur_p]) {
            //     int e_id = item.first;
            //     edge_v.push_back(pair<double,int> (1.0*Edge[e_id].rest/Edge[e_id].degree,e_id));
            // }
            // sort(edge_v.begin(),edge_v.end(),greater<pair<double,int> >() );
            // int num_edge = edge_v.size();
            // unordered_map<int,int> node_sub;
            // cerr<<"p:"<<cur_p<<" "<<num_edge<<endl;
            // for(int i=0;i<num_edge*fac;i++){
            //     int e_id = edge_v[i].second;
            //     check_edge.erase(e_id);
            //     if(Edge[e_id].degree > shield_heavy_node) continue;
            //     for(auto &n_id:Edge[e_id].nodes) {
            //         // node_sub[n_id] ++;
            //         score_list.sub(n_id);
            //     }
            // }
            // for(auto &item:node_sub){
            //     int n_id = item.first;
            //     int val = item.second;
            //     if(val == 0) continue;
            //     score_list.sub(n_id,val);
            // }
            check_edge.clear();
            // for(auto &item:part_edge[cur_p]){
            //     int e_id = item.first;
            //     if(1.0*Edge[e_id].rest/Edge[e_id].degree < fac) continue;
            //     check_edge.erase(e_id);
            // }            
            score_list.clear();
            cur_p += 1;

            part_node.push_back(unordered_set<int>());
            part_edge.push_back(unordered_map<int,int>());   
            time2 += (clock()-beg_t)*1000/CLOCKS_PER_SEC;   
        }
    }
    // cerr<<cur_p<<": "<<"time:"<<(clock()-time1)*1000/CLOCKS_PER_SEC<< " edge num:"<<part_edge[cur_p].size()<<" node num:"<<part_node[cur_p].size()<<endl;

    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<p;i++) {
        vector<int> tmp(11);
        k_1 += part_edge[i].size();
        double ave = 0;
        for(auto &item:part_edge[i]){
            int e_id = item.first;
            double per = 1.0*part_edge[i][e_id]/Edge[e_id].degree;
            ave += per;
            tmp[int(per*10)] ++;
             
        }
        ave /= part_edge[i].size();
        // cerr<<i<<": "<<" edge num:"<<part_edge[i].size()<<" node num:"<<part_node[i].size()<<" ave:"<<ave<<endl;
        // for(int j=0;j<11;j++) cerr<<j<<":"<<tmp[j]<<" ";
        // cerr<<endl;
    }
    cerr<<"cnt_big:"<<cnt_big<<endl;
    cerr<<"parameter:"<<endl<<"p:"<<p<<" shield_heavy_node:"<<shield_heavy_node<<" prob:"<<prob<<" fac:"<<fac<<endl;
    cerr<<"time1:"<<time1<<" "<<"time2:"<<time2<<endl;
    cerr<<"k-1: "<<k_1-m<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
}
int main(){
    // n = 4600;
    // m = 4600;
    // string path = "../data/wiki/wiki.txt";

    n = 56520;
    m = 120870;
    string path = "../data/github/github.txt";

    // n = 901167;
    // m = 34462;
    // string path = "../data/dbpedia-team/out.dbpedia-team";

    // n = 127824;
    // m = 383641;
    // string path = "../data/actor-movie/out.actor-movie";

    // n = 172100;
    // m = 53420;
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

    for(int i=1; i<=10; i++){
        int p = 16;
        int shield_heavy_node = 10000;
        double fac = i*0.1 - 0.1;
        // double prob = 1.0/p;
        double prob = 0;
        for(int j=0;j<m;j++) Edge[j].rest = Edge[j].degree;
        solve(n,m,Node,Edge,p,shield_heavy_node,prob,fac);
    }
    //}

    return 0;
}
