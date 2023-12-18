

#pragma GCC optimize(2)
#include <bits/stdc++.h>
#include <cmath>
#include <stdlib.h>
#include "data.hpp"
#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <cstring>

using namespace std;
int n,m;
HyperNode *Node;
HyperEdge *Edge;
vector<int> nn;
vector<int> mm;
vector<string> filename;
typedef pair<int,int> P;
int Emaxi_degree,Emini_degree;
int total_edge;
unordered_map<int,int> count_E;
class Score_List{
public:
    int maxi_degree;
    int num_node;
    int cur_maxi;
    // HyperNode *Node;
    // HyperEdge *Edge;
    vector<unordered_map<int,int> > degree_mp;
    unordered_map<int,double> Eval;
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
    void add(int id,double val = 1){     
        assert(val>0);
        if(assigned(id)) return;
        int pre_v = Eval[id];
        Eval[id] += val;        
        // cerr<<Eval[id]<<" "<<degree_mp.size()<<endl;
        while(Eval[id]>=degree_mp.size()) degree_mp.push_back(unordered_map<int,int>() );
        assert(Eval[id]<degree_mp.size());
        int aft_v = Eval[id];
        if(pre_v == aft_v) return;
   
        degree_mp[pre_v].erase(id);
        degree_mp[aft_v][id] = 1;

        if(aft_v>cur_maxi) cur_maxi = aft_v;        

    }

    
    int top(){
        if(cur_maxi == 0 &&degree_mp[cur_maxi].size() == 0){
            for(auto &item:wait_assign) return item;
        }
        
        for(auto &item : degree_mp[cur_maxi])  {
            int n_id = item.first;

            // cerr<<"top:"<<n_id<<" cur_maxi:"<<cur_maxi<<endl;
        
            assert(assigned(n_id) == false);
            return n_id; 
        }
        assert(false);
        return -1;
    }
    void erase(int id){
        // cerr<<"erase:"<<id<<endl;
        assert(assigned(id) == false);
        wait_assign.erase(id);
        degree_mp[int(Eval[id])].erase(id);
        if(int(Eval[id]) == cur_maxi) {
            while(cur_maxi != 0 && degree_mp[cur_maxi].size() == 0) cur_maxi --;
        }
    }
    void clear(){
        Eval = unordered_map<int,double>();
        cur_maxi = 0;
        for(int i=0; i< degree_mp.size();i++) degree_mp[i].clear();
    }
};

void load_data(string path,HyperNode * Node,HyperEdge * Edge){
    // swap(n,m);
    FILE *file;
    file = fopen(path.c_str(),"r");
    int n_id,e_id;
    int turn = 0;
    total_edge = 0;
    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        assert(n_id<n);
        assert(e_id<m);
        Node[n_id].edges.push_back(e_id);
        Edge[e_id].nodes.push_back(n_id);
        total_edge++;
    }
}


double cmp(HyperNode node,set<int> edges){
    double ret = 0;
    for(auto  &e_id:node.edges ){
        if(edges.find(e_id) != edges.end()){
            ret +=  -log2(1.0*Edge[e_id].degree/n);
        }
    }
    return ret;
}
void solve(int n,int m,string path, int p,string output = "None"){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // sheild: sheild update edge degree(log)
    // eval function: log 1 or 1/x
    //output: output partition infomation

    Node = new HyperNode[n];
    Edge = new HyperEdge[m];
    clock_t beg_time = clock();
    clock_t tot_begin = clock();
    load_data(path,Node,Edge);
    for(int i=0;i<n;i++) {
        Node[i].id = i; 
        Node[i].degree = Node[i].edges.size();
    }
    vector<int> edge_degree;
    Emaxi_degree = 0;
    Emini_degree = 1e9;
    for(int i=0;i<m;i++) {
        Edge[i].id = i;
        Edge[i].degree = Edge[i].nodes.size();
       
        Emaxi_degree = max(Emaxi_degree,Edge[i].degree); 
        if(Edge[i].degree < 2) continue;
        Emini_degree = min(Emini_degree,Edge[i].degree);
    }
    for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
    sort(edge_degree.begin(),edge_degree.end(),greater<int>());


    int maxi_cap = n/p + 1;
    vector<unordered_map<int,int> > part_node;
    vector<set<int> > part_edge;
    int maxi_degree = 0;



    int cnt = 0;
    int cur_p = 0;
    for(int i = 0; i < p; i++) part_node.push_back(unordered_map<int,int>());
    for(int i = 0; i < p; i++) part_edge.push_back(set<int>());  

    set<int> unalloc;
    for(int i=0;i<n;i++) unalloc.insert(i);
    // double c = total_edge * sheild/(p-1);

    while(cnt < n){   
        cnt ++; 
        int add_node = *(unalloc.begin());
        double val = cmp(Node[add_node],part_edge[cur_p]);
        int cntt = 0;
        for(auto &vid :unalloc){
            double cur_v = cmp(Node[vid],part_edge[cur_p]);
            cntt += 1;
            if(cur_v > val) {
                add_node = vid;
                val = cur_v;
            }
        }
        part_node[cur_p][add_node] = 1;
        std::cout<<cnt<<" "<<add_node<<" "<<cntt<<endl;

        for(auto &e_id:Node[add_node].edges){
            part_edge[cur_p].insert(e_id);
        }
        unalloc.erase(add_node);
        if(part_node[cur_p].size() >= maxi_cap){   
            cur_p += 1;
        }
        

    }
    clock_t end_time = clock();
    int k_1 = 0;
    for(int i=0;i<p;i++) {
        vector<int> tmp(11);
        k_1 += part_edge[i].size();
    }

    clock_t runtime = (end_time-beg_time)*1000/CLOCKS_PER_SEC;
    clock_t tot_time = (clock()-tot_begin)*1000/CLOCKS_PER_SEC;
    std::cout<<"runtime:"<<runtime<<"ms"<<endl;
    std::cout<<"k-1:"<<k_1-m<<endl;
    if(output != "None"){
        FILE *result;
        result = fopen(output.c_str(),"w");
        for(int i=0;i<p;i++){
            for(auto &item:part_node[i]){
                int n_id = item.first;
                fprintf(result,"%d %d\n",n_id,i);
            }
        }
        fclose(result);
    }
    delete []Node;
    delete []Edge;

}

void parsingCmd(int argc,char *argv[]){
    string input="../data/wiki_new.txt";
    n = 4567;
    m = 4132;
    int p = 2;
    string result_path = "./cmd-fun-result.txt";
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
        }else if(std::string(argv[i]) == "-o" && i + 1 < argc){
            result_path = argv[i + 1];
        }else if(std::string(argv[i]) == "-save" && i + 1 < argc){
            save = argv[i + 1];
        }
    }

    freopen(result_path.c_str(),"w",stdout);
    cout<<"parameters:"<<endl;
    cout<<"dataset:"<<input<<"\tn:"<<n<<"\tm:"<<m<<endl;
    cout<<"logFile:"<<result_path<<endl;
    cout<<"save partitionFile:"<<save<<endl;
    solve(n,m,input,p,save);
}
int main(int argc,char *argv[]){
    parsingCmd(argc,argv);
    // string method;
    // method = argv[1];
    // method = "basic";
    // load_dataset();
    // unit_single();
    // unit_basic();
    // unit_entropy();
    // cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
    // cout<<"# p , k-1 , partition time , total time "<<endl; 
    // for(int i=2;i<=64;i*=2){
    // get_partition_result(method);
    // }
    // sheild_select();


    return 0;
}
