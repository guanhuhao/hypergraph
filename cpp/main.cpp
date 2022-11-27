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
    int maxi_size;
    struct cmp{
        bool operator()(P a,P b){
            return a.first > b.first;
        }
    };
public:
    set<int> check;
    priority_queue<P,vector<P>,cmp> heap;
    void add(int rank,int id){
        if(check.find(id) != check.end()) return;
        if(check.size() == maxi_size && heap.top().first<rank){
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
};

// class K_core{
//     void get_kcore(){
//         vector<P> mp_node;
//         vector<>
//     }
// };
HyperNode *Node;
HyperEdge *Edge;
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

void solve(int p,int topk){
    int maxi_cap = n/p + 5;
    vector<set<int> > part_node;
    vector<set<int> > part_edge;
    map<int,int> eval;
    map<int,bool> assign_n; 
    Heap heap(topk);
    int heap_size = 1;

    int cnt = 0;
    int cur_p = 0;
    part_node.push_back(set<int>());
    part_edge.push_back(set<int>());
    clock_t beg_time = clock();
    while(cnt < n){
        cnt += 1;
        // if(cnt%100 == 0) cerr<<cnt<<endl;
        for(int id=0;id<n;id++) {
            if(assign_n[id] == true) continue;
            if(Node[id].degree == 0) continue;
            heap.add(eval[id],id);
        }
        while(heap.size()!=0){
            int cur_node = heap.top();
            heap.pop();
            assign_n[cur_node] = true;
            part_node[cur_p].insert(cur_node);
            for(auto &e_id:Node[cur_node].edges){
                if(part_edge[cur_p].find(e_id) == part_edge[cur_p].end()){
                    part_edge[cur_p].insert(e_id);
                    for(auto &n_id:Edge[e_id].nodes){
                        if(assign_n[n_id] == true) continue;
                        eval[n_id] += 1;
                    }
                }
            }
            if(part_node[cur_p].size() >= maxi_cap){
                cur_p += 1;
                part_node.push_back(set<int>());
                part_edge.push_back(set<int>());
                eval.clear();
            }
        }
    }
    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<part_edge.size();i++) {
        cerr<<i<<":"<<part_node[i].size()<<" "<<part_edge[i].size()<<endl;
        k_1 += part_edge[i].size();
        for(auto &e_id:part_edge[i]) edge_set.insert(e_id);
    }
    cerr<<"para:"<<endl<<"p:"<<p<<" topk:"<<topk<<endl;
    cerr<<"k-1: "<<k_1-edge_set.size()<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
}
int main(){
    n = 4600;
    m = 4600;
    string path = "../data/wiki/wiki.txt";

    // // // n = 56519;
    // // // m = 120867;
    // // // string path = "../data/github/github.txt";

    Node = new HyperNode[n];
    Edge = new HyperEdge[m];
    for(int i=0;i<n;i++) Node[i].id = i;
    for(int i=0;i<m;i++) Edge[i].id = i;

    int p = 16;
    load_data(path);
    solve(p,1);
    printf("OK");

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
