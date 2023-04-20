#include <bits/stdc++.h>
#include <cmath>
#include <stdlib.h>
#include "data.hpp"
// #include "partition.hpp"
using namespace std;
int n,m;
HyperNode *Node;
HyperEdge *Edge;
vector<int> nn;
vector<int> mm;
vector<string> filename;
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

    
    int top(){
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
    // swap(n,m);
    FILE *file;
    file = fopen(path.c_str(),"r");
    int n_id,e_id;
    int turn = 0;
    while(~fscanf(file,"%d%d",&n_id,&e_id)){
        assert(n_id<n);
        // cerr<<e_id<<" "<<m<<endl;
        assert(e_id<m);
        Node[n_id].edges.push_back(e_id);
        Edge[e_id].nodes.push_back(n_id);
    }
}

void solve(int n,int m,string path, int p, int shield_heavy_node = 1e9,double per= -1,bool output = false){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // topk: add topk node at once 
    // buffer_fac: set buffer to reduce search range 
    // shield_heavy_node: shield heavy node to speed and improve quality

    Node = new HyperNode[n];
    Edge = new HyperEdge[m];

    clock_t tot_begin = clock();
    load_data(path,Node,Edge);
    for(int i=0;i<n;i++) {
        Node[i].id = i; 
        Node[i].degree = Node[i].edges.size();
    }
    vector<int> edge_degree;
    for(int i=0;i<m;i++) {
        Edge[i].id = i;
        Edge[i].degree = Edge[i].nodes.size();
    }

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
    clock_t beg_time = clock();

    int cur_deg = tot_deg;
    unordered_map<int,int> check_edge;
    while(cnt < n){   
        cnt ++; 
        int add_node = score_list.top();
        score_list.erase(add_node);
        part_node[cur_p][add_node] = 1;

        for(auto &e_id:Node[add_node].edges){
            part_edge[cur_p][e_id] += 1;
            if(part_edge[cur_p][e_id] == 1){
                check_edge[e_id] += 1;
                if(Edge[e_id].degree > shield_heavy_node) continue;
                for(int i=0;i<Edge[e_id].degree;i++){
                    int n_id = Edge[e_id].nodes[i];
                    score_list.add(n_id);
                }
            }
        }
 
        if(part_node[cur_p].size() >= maxi_cap){   
            score_list.clear();
            cur_p += 1;
            part_node.push_back(unordered_map<int,int>());
            part_edge.push_back(unordered_map<int,int>());   
        }
    }
    // cerr<<cur_p<<": "<<"time:"<<(clock()-time1)*1000/CLOCKS_PER_SEC<< " edge num:"<<part_edge[cur_p].size()<<" node num:"<<part_node[cur_p].size()<<endl;
    clock_t end_time = clock();
    int k_1 = 0;
    set<int> edge_set;
    for(int i=0;i<p;i++) {
        vector<int> tmp(11);
        k_1 += part_edge[i].size();
        // double ave = 0;
        // for(auto &item:part_edge[i]){
        //     int e_id = item.first;
        //     double per = 1.0*part_edge[i][e_id]/Edge[e_id].degree;
        //     ave += per;
        //     tmp[int(per*10)] ++;
             
        // }
        // ave /= part_edge[i].size();
        // cerr<<i<<": "<<" edge num:"<<part_edge[i].size()<<" node num:"<<part_node[i].size()<<" ave:"<<ave<<endl;
        // for(int j=0;j<11;j++) cerr<<j<<":"<<tmp[j]<<" ";
        // cerr<<endl;
    }
    map<int,int> cnt_num;
    map<int,int> cnt_val;
    int maxi_edge_degree = 0;
    int cnt_edge = 0;
    for(int i = 0;i<m;i++){
        int e_id = Edge[i].id;
        int deg = Edge[i].degree;
        if(deg<shield_heavy_node) cnt_edge++;
        cnt_num[deg] ++;
        cnt_val[deg] += check_edge[e_id];
        maxi_edge_degree = max(maxi_edge_degree,deg);
    }
    double sum_val,sum_cnt;
    int gap = 50;
    sum_val = sum_cnt = 0;
    for(int i=0;i<maxi_edge_degree;i++){
        // if(cnt_num[i] == 0) continue;
        if(i%gap == 0 && i != 0){
            if(sum_cnt == 0) continue;
            // cerr<<"degree:"<<i<<" ave:"<<sum_val/sum_cnt<<endl;
            sum_val = sum_cnt = 0;
        }
        sum_cnt += cnt_num[i];
        sum_val += cnt_val[i];
    }
    clock_t runtime = (end_time-beg_time)*1000/CLOCKS_PER_SEC;
    clock_t tot_time = (clock()-tot_begin)*1000/CLOCKS_PER_SEC;
    cerr<<"parameter:"<<endl<<"p:"<<p<<" shield_heavy_node:"<<shield_heavy_node<<endl;
    cerr<<"k-1: "<<k_1-m<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
    cerr<<"sheild%:"<<1.0*cnt_edge/m<<endl;
    cout<<p<<","<<k_1-m<<","<<runtime<<","<<tot_time;
    if(per != -1) cout<<","<<shield_heavy_node<<","<<per;
    cout<<endl;
    if(output){
        FILE *result;
        string result_path = path;
        string filename;
        while (result_path.back()!='/') {
            filename.push_back(result_path.back());
            result_path.pop_back();
        }
        reverse(filename.begin(),filename.end());
        result_path = result_path+"NA-par/"+filename;
        cerr<<"outlog:"<<result_path<<endl;

        result = fopen(result_path.c_str(),"w");
        for(int i=0;i<p;i++){
            for(auto &item:part_node[i]){
                int n_id = item.first;
                for(auto &e_id:Node[n_id].edges){
                    fprintf(result,"%d %d %d\n",n_id,e_id+n,i);
                    fprintf(result,"%d %d %d\n",e_id+n,n_id,i);
                }

            }
        }
    }
}
void unit_test1(){
    freopen("./out/our-base.txt","w",stdout);
    cerr<<"load data OK!"<<endl;
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        cerr<<n<<" "<<m<<endl;
        string path = filename[i];
        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"#| p | k-1 | partition time | total time |"<<endl; 
        for(int p=2; p<=64;p*=2){
            int sheild_heavy_node = 10000000;
            solve(n,m,path,p,sheild_heavy_node);
        }
        cout<<endl;
    }
}

void unit_test2(){
    freopen("./out/our-sheild.txt","w",stdout);
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        string path = filename[i];
        // cerr<<n<<" "<<m<<endl;
        Node = new HyperNode[n];
        Edge = new HyperEdge[m];

        load_data(path,Node,Edge);
        vector<int> edge_degree;
        for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
        sort(edge_degree.begin(),edge_degree.end(),greater<int>());
        // for(int i=0;i<10;i++) cout<<edge_degree[i]<<" ";
        // cout<<endl;

        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
        cout<<"#| p | k-1 | partition time | total time |"<<endl; 
        for(int p=2; p<=64;p*=2){
            int sheild_heavy_node = edge_degree[int(0.01*m)];
            solve(n,m,path,p,sheild_heavy_node);
        }
        cout<<endl;
    }
}

void get_partition_result(int p){
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        string path = filename[i];
        // cerr<<n<<" "<<m<<endl;
        Node = new HyperNode[n];
        Edge = new HyperEdge[m];

        load_data(path,Node,Edge);
        vector<int> edge_degree;
        for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
        sort(edge_degree.begin(),edge_degree.end(),greater<int>());
        // for(int i=0;i<10;i++) cout<<edge_degree[i]<<" ";
        // cout<<endl;

        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
        cout<<"#| p | k-1 | partition time | total time |"<<endl; 
        // int p = 8;
        // for(int p=2; p<=64;p*=2){
            int sheild_heavy_node = edge_degree[int(0.01*m)];
            solve(n,m,path,p,sheild_heavy_node,-1,true);
        // }
        cout<<endl;
    }
}

void sheild_select(){
    // freopen("./out/our-sheild-select.txt","w",stdout);
    freopen("./out/big-data-sheild.txt","w",stdout);
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        string path = filename[i];
        // cerr<<n<<" "<<m<<endl;
        Node = new HyperNode[n];
        Edge = new HyperEdge[m];

        load_data(path,Node,Edge);
        vector<int> edge_degree;
        for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
        sort(edge_degree.begin(),edge_degree.end(),greater<int>());

        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
        cout<<"#| p | k-1 | partition time | total time | shield degree | shield per |"<<endl; 
        int rec_s = -1;
        vector<double> candidate;
        for(int j=2;j<=5;j++) candidate.push_back(0.1*j);
        // for(double j=0.5;j>0.05;j/=1.5) candidate.push_back(j);
        // double tmp = 0.05*m;
        // double fac = pow(tmp,1.0/15);
        // for(double j = 0.05; int(j*m)!=0; j/=fac) candidate.push_back(j);
        int p = 16;

        // for(int p=2; p<=64;p*=2){
            // double tmp = 0.11*m;
            // double fac = pow(tmp,1.0/20);
            // cerr<<"fac:"<<fac<<endl;
            // for(double j = 0.1; int(j*m)!=0; j/=fac){
            for(auto &j:candidate){
                int sheild_heavy_node = edge_degree[int(j*m)];
                // if(rec_s == sheild_heavy_node) continue;
                rec_s = sheild_heavy_node;
                solve(n,m,path,p,sheild_heavy_node,j);
            }
        // }
        cout<<endl;
    }
}
int main(){
    // nn.push_back( 127823 );
    // mm.push_back( 383640 );
    // filename.push_back( "../data/out.actor-movie" );

    // nn.push_back( 383640 ); // use
    // mm.push_back( 127823 );
    // filename.push_back( "../data/out.actor-movie-swap.txt" );

    // nn.push_back( 1953085 );// use
    // mm.push_back( 5624219 );
    // filename.push_back( "../data/out.dblp-author" );

    // nn.push_back( 5623931 );
    // mm.push_back( 1953085 );
    // filename.push_back( "../data/out.dblp-author-swap.txt" );

    nn.push_back( 172091 );
    mm.push_back( 53407 );
    filename.push_back( "../data/out.dbpedia-location" );

    // nn.push_back( 53407 ); //use
    // mm.push_back( 172091 );
    // filename.push_back( "../data/out.dbpedia-location-swap.txt" );

    // nn.push_back( 901166 );
    // mm.push_back( 34461 );
    // filename.push_back( "../data/out.dbpedia-team" );

    // nn.push_back( 34461 ); //use
    // mm.push_back( 901166 );
    // filename.push_back( "../data/out.dbpedia-team-swap.txt" );

    // nn.push_back( 56519 );
    // mm.push_back( 120867 );
    // filename.push_back( "../data/out.github" );

    // nn.push_back( 120867 );
    // mm.push_back( 56519 );
    // filename.push_back( "../data/out.github-swap.txt" );

    // nn.push_back( 2783196 );
    // mm.push_back( 8730857 );
    // filename.push_back( "../data/out.orkut-groupmemberships" );

    // nn.push_back( 8730857 );
    // mm.push_back( 2783196 );
    // filename.push_back( "../data/out.orkut-groupmemberships-swap.txt" );

    // nn.push_back( 27665730 );
    // mm.push_back( 12756244 );
    // filename.push_back( "../data/out.trackers" );

    // nn.push_back( 12756244 );
    // mm.push_back( 27665730 );
    // filename.push_back( "../data/out.trackers-swap.txt" );

    // nn.push_back( 4566 );
    // mm.push_back( 4131 );
    // filename.push_back( "../data/wiki_new.txt" );

    // nn.push_back( 4131 );
    // mm.push_back( 4566 );
    // filename.push_back( "../data/wiki_new.txt-swap.txt" );

    // nn.push_back( 10000000 );
    // mm.push_back( 10000000 );
    // filename.push_back( "../data/rand-n10M-m10M-e100M" );


    unit_test1();
    // unit_test2();
    // sheild_select();
    int p = 8;
    // get_partition_result(p);

    return 0;
}
