#include <bits/stdc++.h>
using namespace std;
typedef pair<int,int> P; 
int n,m;
class HyperNode{
public:
    int id;
    int degree;
    vector<int> edges;
};
class HyperEdge{
public:
    int id;
    int degree;
    vector<int> nodes;
};
class Buffer{
    struct MinHeap{
        bool operator()(P a,P b){
            return a.first > b.first;
        }
    };
    static bool cmp(const P &a,const P &b){
        return a.first > b.first;
    }

public:
    int maxi_size;
    unordered_map<int,int> *eval;
    set<int> check;
    vector<P> heap;
    void add(int id){
        //  make_heap(heap.begin(),heap.end());
        if(check.find(id) != check.end()) return;
        if(check.size() == maxi_size && heap[0].first >= (*eval)[id]) return;
        if(check.size() == maxi_size && heap[0].first <  (*eval)[id]){
            pop_heap(heap.begin(),heap.end(),cmp);
            int remove_id = heap.back().second;
            heap.pop_back();
            check.erase(remove_id);
        }
        heap.push_back(P((*eval)[id],id));
        push_heap(heap.begin(),heap.end(),cmp);
        check.insert(id);
    }
    vector<int> get_topk(int k){
        priority_queue<P,vector<P>,MinHeap> topk;
        for(auto &n_id:check){
            if(topk.size()<k){
                topk.push(P((*eval)[n_id],n_id));
                continue;
            }
            if(topk.size() == k && topk.top().first<(*eval)[n_id]){
                topk.pop();
                topk.push(P((*eval)[n_id],n_id));
            }
        }
        vector<int> ret;
        while(topk.size()!=0) {
            int id = topk.top().second;
            ret.push_back(id);
            topk.pop();
        }
        return ret;
    }
    Buffer(int m_size ,std::unordered_map<int,int> *E){
        this->eval = E;
        this->maxi_size = m_size;
    }
    void erase(int id){
        check.erase(id);
    }
    void rebuild(){
        heap.clear();
        heap.resize(check.size());
        int i = 0;
        for(auto &n_id:check) heap[i++] = P((*eval)[n_id],n_id);
        make_heap(heap.begin(),heap.end());
    }
    bool exist(int id){
        return check.find(id) != check.end();
    } 
    int size(){
        return check.size();
    }
    // int top(){
    //     assert(heap.size() != 0);
    //     return heap.top().second;
    // }
    void clear(){
        check.clear();
        heap.clear();
    }
};

HyperNode *Node;
HyperEdge *Edge;
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
            // cerr<<"k:"<<k<<" rest:"<<nex_n->size()<<endl;
            if(nex_n->size() == 0) return del_node;
            
            for(auto &n_id:del_node){
                for(auto &e_id:Node[n_id].edges){
                    // cerr<<mp_edge[e_id]<<endl;
                    // assert(mp_edge[e_id] > 0);
                    mp_edge[e_id] -= 1;
                }
            }

            for(auto &e_id:del_edge){
                for(auto &n_id:Edge[e_id].nodes){
                    // assert(mp_node[n_id] > 0);
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
void load_data(string path){
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

void solve(int p,int topk, int buffer_fac = 2){
    int maxi_cap = n/p + 1;
    vector<set<int> > part_node;
    vector<set<int> > part_edge;
    unordered_map<int,int> eval;
    unordered_map<int,bool> assign_n; 
    int buffer_size = topk*buffer_fac;
    Buffer buffer(buffer_size,&eval);
    // K_core kcore(Node,Edge,n,m);
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
        Buffer heap(topk,&eval);
        for(int i=0;i<n;i++){
            if(assign_n[i] == true) continue;
            heap.add(i);
            // if(add_node.size() == 0) add_node.push_back(i);
            // if(eval[i]>eval[add_node[0]]) add_node[0] = i;
        }
        // if(part_node[cur_p].size()==0){
        //     add_node = kcore.get_kcore();
        // }else{
        //     beg = clock();
        //     if(buffer.size()<buffer_size/2){
        //         buffer.clear();
        //         for(int id=0;id<n;id++) {
        //             if(assign_n[id] == true) continue;
        //             buffer.add(id);
        //         }
        //     }
        //     for(auto &id:buffer.get_topk(topk)){
        //         add_node.push_back(id);
        //     }
        //     timer1 += (clock()-beg)*1000/CLOCKS_PER_SEC;
        // }
        beg = clock();
        // reverse(add_node.begin(),add_node.end());
        // set<int> tmp;
        for(auto &n_id:heap.heap) add_node.push_back(n_id.second);
        for(auto &cur_node:add_node){  
            assert(assign_n[cur_node] == false);   
            // cerr<<"test:"<<cur_node<<endl;
            assign_n[cur_node] = true;
            cnt += 1;   
            if(cnt%1000 == 0) cerr<<"turn "<< cnt<<endl;
            // buffer.erase(cur_node);
            // kcore.del_node(cur_node);
            part_node[cur_p].insert(cur_node);
            for(auto &e_id:Node[cur_node].edges){
                if(part_edge[cur_p].find(e_id) == part_edge[cur_p].end()){
                    part_edge[cur_p].insert(e_id);
                    for(auto &n_id:Edge[e_id].nodes){
                        if(assign_n[n_id] == true) continue;
                        loop += 1;
                        eval[n_id] += 1;
                        // tmp.insert(n_id);
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
                // buffer.clear();
        }
        // buffer.rebuild();
        // for(auto &n_id:tmp) buffer.add(n_id);
        
        timer2 += (clock()-beg)*1000/CLOCKS_PER_SEC;

        // vector<int> rebuild;
        // while(heap.size()!=0) rebuild.push_back(heap.pop());
        // for(auto &n_id:rebuild){
        //     heap.add(eval[n_id],n_id);
        // }
        

    }
    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<part_edge.size();i++) {
        cerr<<i<<":"<<part_node[i].size()<<" "<<part_edge[i].size()<<endl;
        k_1 += part_edge[i].size();
        for(auto &e_id:part_edge[i]) edge_set.insert(e_id);
    }
    cerr<<"para:"<<endl<<"p:"<<p<<" topk:"<<topk<<" buffer_fac:"<<buffer_fac<<endl;
    cerr<<"timer1:"<<timer1<<" timer2:"<<timer2<<" timer3:"<<timer3<<endl;
    cerr<<"loop:"<<loop<<endl;
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
    load_data(path);

    for(int i=0; i<10; i++){
        int p = 16;
        int topk = (i+1)*10;
        int buffer_fac = 2;
        solve(p,topk,buffer_fac);
    }

    // unordered_map<int,int> mp;
    // Buffer test(5,&mp);
    // for(int i=0;i<10;i++) {
    //     mp[i] = i;
    //     test.add(i);
    //     // cerr<<"size:"<<test.heap.size()<<" "<<test.top()<<endl;
    //     cerr<<i<<": ";
    //     for(auto &n_id:test.heap) cerr<<n_id.second<<" ";
    //     cerr<<endl;
    // }
    // for(auto &n_id:test.heap) cerr<<n_id.second<<" ";
    // cerr<<endl;
    
    // vector<int> result = test.get_topk(3);
    // for(int i=0;i<result.size();i++) {
    //     cerr<<result[i]<<endl;
    //     test.erase(result[i]);
    // }    
    // result = test.get_topk(1);
    // for(int i=0;i<result.size();i++) {
    //     cerr<<result[i]<<endl;
    //     test.erase(result[i]);
    // }    
    // cerr<<"size:"<<test.heap.size()<<" "<<test.top()<<endl;
    return 0;
}
