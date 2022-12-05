#include <bits/stdc++.h>
#include "data.h"
#include "buffer.hpp"
#include "k_core.hpp"

using namespace std;
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

void solve(int n,int m, HyperNode *Node, HyperEdge *Edge, int p,int topk, int buffer_fac = 2,bool set_kcore = false){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // topk: add topk node at once 
    // buffer_fac: set buffer to reduce search range 

    int maxi_cap = n/p + 1;
    vector<set<int> > part_node;
    vector<set<int> > part_edge;
    unordered_map<int,int> eval;
    unordered_map<int,bool> assign_n; 
    int buffer_size = topk*buffer_fac;
    Buffer buffer(buffer_size,&eval);
    K_core kcore(Node,Edge,n,m);
    // vector<int> a = kcore.get_kcore();
    int cur_buf = 0;


    int cnt = 0;
    int cur_p = 0;
    part_node.push_back(set<int>());
    part_edge.push_back(set<int>());
    clock_t beg_time = clock();
    clock_t timer1 = 0;
    clock_t timer2 = 0;
    clock_t timer3 = 0;
    int loop = 0;
    while(cnt < n){
        vector<int> add_node;            
        clock_t beg;
        if(part_node[cur_p].size()==0 && set_kcore == true){
            add_node = kcore.get_kcore();
        }else{
            beg = clock();
            if(buffer.size()< topk){
                buffer.clear();
                for(int id=0;id<n;id++) {
                    if(assign_n[id] == true) continue;
                    buffer.add(id);
                }
            }
            for(auto &id:buffer.get_topk(topk)){
                add_node.push_back(id);
            }
            timer1 += (clock()-beg)*1000/CLOCKS_PER_SEC;
        }
        beg = clock();
        reverse(add_node.begin(),add_node.end());
        set<int> tmp;
        for(auto &cur_node:add_node){     
            assign_n[cur_node] = true;
            cnt += 1;   
            buffer.erase(cur_node);
            kcore.del_node(cur_node);
            part_node[cur_p].insert(cur_node);
            for(auto &e_id:Node[cur_node].edges){
                if(part_edge[cur_p].find(e_id) == part_edge[cur_p].end()){
                    part_edge[cur_p].insert(e_id);
                    for(auto &n_id:Edge[e_id].nodes){
                        if(assign_n[n_id] == true) continue;
                        loop += 1;
                        eval[n_id] += 1;
                        tmp.insert(n_id);
                    }
                }
            }
            if(part_node[cur_p].size() >= maxi_cap) break;
 
        }
        if(part_node[cur_p].size() >= maxi_cap){
                cur_p += 1;
                part_node.push_back(set<int>());
                part_edge.push_back(set<int>());
                eval.clear();
                buffer.clear();
        }
        buffer.rebuild();
        for(auto &n_id:tmp) buffer.add(n_id);
        
        timer2 += (clock()-beg)*1000/CLOCKS_PER_SEC;       

    }
    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<part_edge.size();i++) {
        // cerr<<i<<":"<<part_node[i].size()<<" "<<part_edge[i].size()<<endl;
        k_1 += part_edge[i].size();
        for(auto &e_id:part_edge[i]) edge_set.insert(e_id);
    }
    cerr<<"parameter:"<<endl<<"p:"<<p<<" topk:"<<topk<<" buffer_fac:"<<buffer_fac<<endl;
    cerr<<"timer1:"<<timer1<<" timer2:"<<timer2<<" timer3:"<<timer3<<endl;
    cerr<<"loop:"<<loop<<endl;
    cerr<<"k-1: "<<k_1-edge_set.size()<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
}