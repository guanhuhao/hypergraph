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
class Heap{
    struct cmp{
        bool operator()(P a,P b){
            return a.first > b.first;
        }
    };
public:
    int maxi_size;
    set<int> check;
    priority_queue<P,vector<P>,cmp> heap;
    void add(int rank,int id){
        if(check.find(id) != check.end()) return;
        if(check.size() == maxi_size && heap.top().first >= rank) return;
        if(check.size() == maxi_size && heap.top().first < rank){
            this->pop();
        }
        heap.push(P(rank,id));
        check.insert(id);
    }
    Heap(int m_size = 10){
        this->maxi_size = m_size;
    }
    int pop(){
        assert(heap.size() != 0);
        // if(size() == 0) return -1;
        int id = heap.top().second;
        heap.pop();
        check.erase(id);
        return id;
    }
    bool exist(int id){
        return check.find(id) != check.end();
    } 
    int size(){
        return check.size();
    }
    int top(){
        assert(heap.size() != 0);
        return heap.top().second;
    }
    void clear(){
        check.clear();
        heap = priority_queue<P,vector<P>,cmp>();
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
    Heap heap(topk);
    K_core kcore(Node,Edge,n,m);
    // vector<int> a = kcore.get_kcore();
    vector<int> buffer[2];
    int cur_buf = 0;


    int cnt = 0;
    int cur_p = 0;
    part_node.push_back(set<int>());
    part_edge.push_back(set<int>());
    clock_t beg_time = clock();
    clock_t timer1 = 0;
    clock_t timer2 = 0;
    int loop = 0;
    while(cnt < n){
        vector<int> add_node;            
        clock_t beg;
        if(part_node[cur_p].size()==0){
            add_node = kcore.get_kcore();
        }else{
            beg = clock();
            if(buffer[cur_buf].size()<buffer_size/2){
                buffer[cur_buf].clear();
                heap.clear();
                heap.maxi_size = buffer_size;
                for(int id=0;id<n;id++) {
                    if(assign_n[id] == true) continue;
                    heap.add(eval[id],id);
                }
                while(heap.size() != 0) buffer[cur_buf].push_back(heap.pop());
                heap.maxi_size = topk;
            }
            assert(heap.size()==0);
            for(auto &n_id:buffer[cur_buf]) heap.add(eval[n_id],n_id);
            unordered_map<int,int> remove_n;
            while(heap.size()!=0) {
                int n_id = heap.pop();
                add_node.push_back(n_id);
                remove_n[n_id] = 1;
            }
            int nex_buf = cur_buf^1;
            buffer[nex_buf].clear();
            for(auto &n_id:buffer[cur_buf]){
                if(remove_n[n_id] == 1) continue;
                buffer[nex_buf].push_back(n_id);
            }
            cur_buf = nex_buf;
            timer1 += (clock()-beg)*1000/CLOCKS_PER_SEC;
        }
        beg = clock();
        for(auto &cur_node:add_node){     
            
            assign_n[cur_node] = true;
            cnt += 1;   
            kcore.del_node(cur_node);
            part_node[cur_p].insert(cur_node);
            for(auto &e_id:Node[cur_node].edges){
                if(part_edge[cur_p].find(e_id) == part_edge[cur_p].end()){
                    part_edge[cur_p].insert(e_id);
                    for(auto &n_id:Edge[e_id].nodes){
                        if(assign_n[n_id] == true) continue;
                        loop += 1;
                        eval[n_id] += 1;
                    }
                }
            }
            if(part_node[cur_p].size() >= maxi_cap){
                cur_p += 1;
                part_node.push_back(set<int>());
                part_edge.push_back(set<int>());
                eval.clear();
                heap.clear();
                break;
            }        
        }
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
        // cerr<<i<<":"<<part_node[i].size()<<" "<<part_edge[i].size()<<endl;
        k_1 += part_edge[i].size();
        for(auto &e_id:part_edge[i]) edge_set.insert(e_id);
    }
    cerr<<"para:"<<endl<<"p:"<<p<<" topk:"<<topk<<" buffer_fac:"<<buffer_fac<<endl;
    cerr<<"timer1:"<<timer1<<" timer2:"<<timer2<<endl;
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
        int topk = i+1;
        int buffer_fac = 2;
        solve(p,topk,buffer_fac);
        // printf("OK");
    }

    // Heap test(5);
    // for(int i=0;i<10;i++) {
    //     test.add(i,i);
    //     cerr<<"size:"<<test.heap.size()<<" "<<test.top()<<endl;
    // }

    // for(int i=0;i<10;i++) {
    //     cerr<<test.top()<<endl;
    //     test.pop();
    //     cerr<<"size:"<<test.heap.size()<<endl;
    // }    
    // test.add(2,2);
    // cerr<<"size:"<<test.heap.size()<<" "<<test.top()<<endl;
    return 0;
}
