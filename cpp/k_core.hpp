#include <bits/stdc++.h>
#include "data.h"
using namespace std;
class K_core{
    int node_num,edge_num;
    unordered_map<int,int> n_deg,e_deg;
    HyperNode *Node;
    HyperEdge *Edge;
    
public:
    K_core(HyperNode *node,HyperEdge *edge,int n,int m){
         node_num = n;
         edge_num = m;
         Node = node;
         Edge = edge;
         for(int i=0;i<node_num;i++) n_deg[i] = Node[i].degree;
         for(int i=0;i<edge_num;i++) e_deg[i] = Edge[i].degree;
    }
    vector<int> get_kcore(){
        vector<int> ret;
        unordered_map<int,int> mp_node,mp_edge;
        vector<int> *cur_n,*nex_n;
        vector<int> *cur_e,*nex_e;
        vector<int> n_a,n_b;
        vector<int> e_a,e_b;
        cur_n = &n_a;
        nex_n = &n_b;
        cur_e = &e_a;
        nex_e = &e_b;
        for(int i=0;i<node_num;i++) {
            if(n_deg[i] < 0) continue;
            mp_node[i] = n_deg[i];
            cur_n->push_back(i);
        }
        for(int i=0;i<edge_num;i++) {
            if(e_deg[i] < 0) continue;
            mp_edge[i] = e_deg[i];
            cur_e->push_back(i);
        }

        int k = 0;
        while(true){
            vector<int> del_node;
            vector<int> del_edge;
            for(auto &n_id:*cur_n){
                if(mp_node[n_id]<=k) del_node.push_back(n_id);
                else nex_n->push_back(n_id);
            }
            for(auto &e_id:*cur_e){
                if(mp_edge[e_id]<=k) del_edge.push_back(e_id);
                else nex_e->push_back(e_id);
            }
            if(nex_n->size() == 0) {
                vector<int> ret;
                unordered_map<int,int> exist;
                ret.push_back(del_node[0]);
                for(auto &e_id:Node[ret[0]].edges){
                    set<int> n_set;
                    for(auto &n_id:Edge[e_id].nodes) n_set.insert(n_id);
                    for(int i=1;i<del_node.size();i++){
                        if(exist[i] == 1) continue;
                        if(n_set.find(del_node[i]) != n_set.end()) {
                            ret.push_back(del_node[i]);
                            exist[i] = 1;
                        }
                    }
                    return ret;
                }
                return del_node;
            }
            
            for(auto &n_id:del_node){
                for(auto &e_id:Node[n_id].edges){
                    mp_edge[e_id] -= 1;
                }
            }

            for(auto &e_id:del_edge){
                for(auto &n_id:Edge[e_id].nodes){
                    mp_node[n_id] -= 1;
                }
            }

            swap(cur_n,nex_n);
            swap(cur_e,nex_e);
            nex_n->clear();
            nex_e->clear();
            k+=1 ;
        }
        return ret;
    }

    void del_node(vector<int> del_nodes){
        for(auto &n_id:del_nodes){
            for(auto &e_id:Node[n_id].edges){
                e_deg[e_id] -= 1;
            }
            n_deg[n_id] = -1;
        }
    }
    void del_node(int del_nodes){
        for(auto &e_id:Node[del_nodes].edges){
            e_deg[e_id] -= 1;
        }
        n_deg[del_nodes] = -1;
    }
};