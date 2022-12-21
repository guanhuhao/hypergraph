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
    vector<unordered_map<int,int> > degree_mp;
    unordered_map<int,int> Eval;
    unordered_set<int> wait_assign;
    Score_List(int Maxi_degree,int Num_node){
        cur_maxi = 0;
        this->maxi_degree = Maxi_degree;
        this->num_node = Num_node;
        for(int i=0; i<=Maxi_degree;i++){
            degree_mp.push_back(unordered_map<int,int>());
        }
        for(int i=0;i<num_node;i++) wait_assign.insert(i);
    }
    bool assigned(int id){
        return wait_assign.find(id) == wait_assign.end();
    }
    void add(int id){     
        // cerr<<"test2"<<endl;
        if(assigned(id)) return;
        int pre_v = Eval[id];
        Eval[id] ++;
        int aft_v = Eval[id];
   
        if(pre_v!=0) degree_mp[pre_v].erase(id);
        degree_mp[aft_v][id] = 1;
        if(aft_v>cur_maxi) cur_maxi = aft_v;
    }

    // void sub(int id,int val=1){
    //     if(assign[id] == true) return;
    //     int pre_v = Eval[id];
    //     Eval[id] -=val;
    //     int aft_v = Eval[id];
    //     degree_mp[pre_v].erase(id);
    //     degree_mp[aft_v][id] = 1;
    //     while(cur_maxi != 0 && degree_mp[cur_maxi].size() == 0) cur_maxi --;
    // }
    
    int top(){
        // if(degree_mp[cur_maxi].size() == 0) return -1;
        if(cur_maxi == 0 &&degree_mp[cur_maxi].size() == 0){
            for(auto &item:wait_assign) return item;
        }
        for(auto &item : degree_mp[cur_maxi])  {
            int n_id = item.first;
            assert(assigned(n_id) == false);
            return n_id; 
        }
        return -1;
    }
    void erase(int id){
        assert(assigned(id) == false);
        wait_assign.erase(id);

        degree_mp[Eval[id]].erase(id);
        if(Eval[id] == cur_maxi) {
            while(cur_maxi != 0 && degree_mp[cur_maxi].size() == 0) cur_maxi --;
        }
    }
    void clear(){
        Eval = unordered_map<int,int>();
        cur_maxi = 0;
        for(int i=0; i<=maxi_degree;i++) degree_mp[i].clear();
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
    double tot_deg = 0;
    for(int i = 0; i<n; i++) 
        maxi_degree = max(Node[i].degree,maxi_degree);

    Score_List score_list(maxi_degree,n);
    int cnt = 0;
    int cur_p = 0;
    part_node.push_back(unordered_map<int,int>());
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

        beg_t = clock();
        score_list.erase(add_node);
        part_node[cur_p][add_node] = 1;

        for(auto &e_id:Node[add_node].edges){
            part_edge[cur_p][e_id] += 1;
            // Edge[e_id].rest--;
            // if(Edge[e_id].rest < Edge[e_id].degree/2){
            //     int pos = 0;
            //     for(auto &n_id:Edge[e_id].nodes){
            //         if(score_list.assigned(n_id)) continue;
            //         Edge[e_id].nodes[pos] = n_id;
            //         pos++;
            //     }
            //     Edge[e_id].nodes.resize(Edge[e_id].rest);
            //     Edge[e_id].degree = Edge[e_id].rest;
            // }
            if(part_edge[cur_p][e_id] == 1){
                if(Edge[e_id].degree > shield_heavy_node) continue;
                for(auto &n_id:Edge[e_id].nodes) {
                    score_list.add(n_id);
                }
            }
        }
        
        time1 += (clock()-beg_t)*1000/CLOCKS_PER_SEC;
 
        if(part_node[cur_p].size() >= maxi_cap){
            beg_t = clock();     
            score_list.clear();
            cur_p += 1;
            part_node.push_back(unordered_map<int,int>());
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
    clock_t runtime = (end_time-beg_time)*1000/CLOCKS_PER_SEC;
    cerr<<"cnt_big:"<<cnt_big<<endl;
    cerr<<"parameter:"<<endl<<"p:"<<p<<" shield_heavy_node:"<<shield_heavy_node<<endl;
    cerr<<"time1:"<<time1<<" "<<"time2:"<<time2<<endl;
    cerr<<"k-1: "<<k_1-m<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
    cout<<p<<" "<<shield_heavy_node<<" "<<k_1-m<<" "<<runtime<<endl;
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

    // n = 127824;
    // m = 383641;
    // string path = "../data/actor-movie/out.actor-movie";

    n = 172100;
    m = 53420;
    string path = "../data/dbpedia-location/out.dbpedia-location";
    
    // n = 1953086;
    // m = 5624220;
    // string path = "../data/dblp-author/out.dblp-author";
    string filename;
    for(auto &ch:path){
        filename.push_back(ch);
        if(ch == '/') filename.clear();
    }
    string out_path = "./out/"+filename+".log";

    freopen(out_path.c_str(),"w",stdout);


    Node = new HyperNode[n];
    Edge = new HyperEdge[m];

    cerr<<"begin load data!"<<endl;
    load_data(path,Node,Edge);
    for(int i=0;i<n;i++) {
        Node[i].id = i; 
        Node[i].degree = Node[i].edges.size();
    }
    for(int i=0;i<m;i++) {
        Edge[i].id = i;
        Edge[i].degree = Edge[i].rest = Edge[i].nodes.size();
    }
    cerr<<"load data OK!"<<endl;
    cout<<"# dataset:"<<filename<<endl;
    cout<<"# p sheild k-1 runtime(ms)"<<endl;
    for(int i=1; i<= 6; i++){
        int p = 1 << i;
        int shield_heavy_node = 1e9;
        solve(n,m,Node,Edge,p,shield_heavy_node);
    }
    //}

    return 0;
}
