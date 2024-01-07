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
        // cerr<<e_id<<" "<<m<<endl;
        assert(e_id<m);
        Node[n_id].edges.push_back(e_id);
        Edge[e_id].nodes.push_back(n_id);
        total_edge++;
    }
}

void solve(int n,int m,string path, int p,double sheild = 0,string method = "entropy",string output = "None"){
    // n: number of HyperNode
    // m: number of HyperEdge
    // Node: array of HyperNode
    // Edge: array of HyperEdge
    // p: number of partition 
    // sheild: sheild update edge degree(log)
    // eval function: log 1 or 1/x
    //output: output partition infomation
    cerr<<"parameters:\nn:"<<n<<" m:"<<m<<" path:"<<path<<" p:"<<p<<" output:"<<output<<endl;

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
    vector<unordered_map<int,int> > part_edge;
    int maxi_degree = 0;


    Score_List score_list(maxi_degree,n);
    cerr<<"method:"<<method<<endl;
    if(method == "anti-basic"){
        int max_val = -1;
        int cnt = 0;
        for(int i=0;i<n;i++) max_val = max(max_val,int(Node[i].edges.size())+1);
        for(int i=0;i<n;i++){
            // cerr<<i<<" "<<max_val-Node[i].edges.size()<<" "<<Emaxi_degree<<" "<<Node[i].edges.size()<<endl;
            score_list.add(i,max_val-Node[i].edges.size());
        }
    }

    int cnt = 0;
    int cur_p = 0;
    for(int i = 0; i < p; i++) part_node.push_back(unordered_map<int,int>());
    for(int i = 0; i < p; i++) part_edge.push_back(unordered_map<int,int>());    
    
    if(method == "random"){
        for(int i = 0 ; i < n; i++){
            int send_p = rand()%p;
            part_node[send_p][i] = 1;
            for(auto &e_id:Node[i].edges){
                part_edge[send_p][e_id] = 1;
            }
        }
    }
    else{
        unordered_map<int,int> check_edge;
        // sheild = 0.2;
        double c = total_edge * sheild;
        // double c = total_edge * sheild/(p-1);
        int pos = 0;
        while(c>0) c -= edge_degree[pos++];
        
        sheild = edge_degree[pos];
        // cerr<<"sheild:"<<sheild<<" "<<pos<<" "<<total_edge<<endl;
    
        clock_t beg_time = clock();

        while(cnt < n){   
            cnt ++; 
            int add_node = score_list.top();
            score_list.erase(add_node);
            part_node[cur_p][add_node] = 1;

            for(auto &e_id:Node[add_node].edges){
                part_edge[cur_p][e_id] += 1;
                if(Edge[e_id].degree>sheild) continue;
                if(part_edge[cur_p][e_id] == 1){
                    double val ;
                    if(method == "entropy") val = -log2(1.0*Edge[e_id].degree/(Emaxi_degree+1));
                    else if (method == "basic") val = 1; 
                    else if (method == "anti-basic") val = 1; 
                    else assert(false);

                    for(int i=0;i<Edge[e_id].degree;i++){
                        int n_id = Edge[e_id].nodes[i];
                        score_list.add(n_id,val);
                    }
                }
            }
            if(part_node[cur_p].size() >= maxi_cap){   
                score_list.clear();
                cur_p += 1;
            }
        }

    }
    clock_t end_time = clock();
    int k_1 = 0;
    for(int i=0;i<p;i++) {
        vector<int> tmp(11);
        k_1 += part_edge[i].size();
    }
    // map<int,int> cnt_num;
    // map<int,int> cnt_val;
    // int maxi_edge_degree = 0;
    // int cnt_edge = 0;
    // for(int i = 0;i<m;i++){
    //     int e_id = Edge[i].id;
    //     int deg = Edge[i].degree;
    //     cnt_num[deg] ++;
    //     cnt_val[deg] += check_edge[e_id];
    //     maxi_edge_degree = max(maxi_edge_degree,deg);
    // }
    // double sum_val,sum_cnt;
    // int gap = 50;
    // sum_val = sum_cnt = 0;
    // for(int i=0;i<maxi_edge_degree;i++){
    //     if(i%gap == 0 && i != 0){
    //         if(sum_cnt == 0) continue;
    //         sum_val = sum_cnt = 0;
    //     }
    //     sum_cnt += cnt_num[i];
    //     sum_val += cnt_val[i];
    // }
    clock_t runtime = (end_time-beg_time)*1000/CLOCKS_PER_SEC;
    clock_t tot_time = (clock()-tot_begin)*1000/CLOCKS_PER_SEC;
    cerr<<"parameter:"<<endl<<"p:"<<p<<endl;
    cerr<<"k-1: "<<k_1-m<<" runtime:"<<(end_time-beg_time)*1000/CLOCKS_PER_SEC<<"(ms)"<<endl<<"----------"<<endl;
    cout<<p<<","<<k_1-m<<","<<runtime<<","<<tot_time;

    cout<<endl;
    if(output != "None"){
        FILE *result;
        // reverse(filename.begin(),filename.end());
        // result_path = result_path+"NA-par/"+filename;
        // cerr<<"outlog:"<<result_path<<endl;

        result = fopen(output.c_str(),"w");
        for(int i=0;i<p;i++){
            for(auto &item:part_node[i]){
                int n_id = item.first;
                fprintf(result,"%d %d\n",n_id,i);
                // for(auto &e_id:Node[n_id].edges){
                //     fprintf(result,"%d %d %d\n",n_id,i);
                //     // fprintf(result,"%d %d %d\n",e_id+n,n_id,i);
                // }

            }
        }
        fclose(result);
    }
    delete []Node;
    delete []Edge;

}
void unit_single(){
    freopen("./out/our-base.txt","w",stdout);
    cerr<<"load data OK!"<<endl;
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        cerr<<n<<" "<<m<<endl;
        string path = "../data/" + filename[i];
        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 , partition time , total time "<<endl; 
        for(int p=16; p<=16;p*=2){
            solve(n,m,path,p);
        }
        cout<<endl;
    }
}
void unit_basic(){
    freopen("./out/our-base-plus1.txt","w",stdout);
    double shield = 0;
    string method = "basic";
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        cerr<<n<<" "<<m<<endl;
        string path = "../data/" + filename[i];
        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 , partition time , total time "<<endl; 
        for(int p=2; p<=64;p*=2){
            solve(n,m,path,p,shield,method);
        }
        cout<<endl;
    }
}
void unit_entropy(){
    double shield = 0.2;
    string method = "entropy";
    // string method = "basic";
    string result = "./out/our-"+string(method)+"-"+to_string(shield)+".txt";
    freopen(result.c_str(),"w",stdout);
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        cerr<<n<<" "<<m<<endl;
        string path = "../data/" + filename[i];
        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 , partition time , total time "<<endl; 
        for(int p=2; p<=64;p*=2){
            solve(n,m,path,p,shield,method);
        }
        cout<<endl;
    }
}

void get_partition_result(string method="entropy"){
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        string path = "../data/" + filename[i];
        // cerr<<n<<" "<<m<<endl;
        Node = new HyperNode[n];
        Edge = new HyperEdge[m];

        load_data(path,Node,Edge);
        vector<int> edge_degree;
        for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
        sort(edge_degree.begin(),edge_degree.end(),greater<int>());
        // for(int i=0;i<10;i++) cout<<edge_degree[i]<<" ";
        // cout<<endl;

        cout<<"# dataset:"<<filename[i]<<" n:"<<n<<" m:"<<m<<endl;
        cout<<"# p , k-1 , partition time , total time "<<endl; 

        string result_path = path;
        string filename;
        while (result_path.back()!='/') {
            filename.push_back(result_path.back());
            result_path.pop_back();
        }
        reverse(filename.begin(),filename.end());
        cerr<<"outlog:"<<result_path<<endl;

        // int p = 8;
        for(int p=2; p<=256;p*=2){
            double sheild_heavy_node = 0;
            result_path = "/raid/guan/large-cluster/comm/test_data/"+to_string(p)+"/"+filename+"/"+method+".txt";
            result_path = "None";
            solve(n,m,path,p,sheild_heavy_node,method,result_path);
        }
        cout<<endl;
    }
}

void sheild_select(){
    // freopen("./out/our-sheild-select.txt","w",stdout);
    freopen("./out/big-data-sheild.txt","w",stdout);
    for(int i=0;i<nn.size();i++){
        n = nn[i]+5;
        m = mm[i]+5;
        string path = "../data/" + filename[i];
        // cerr<<n<<" "<<m<<endl;
        Node = new HyperNode[n];
        Edge = new HyperEdge[m];

        load_data(path,Node,Edge);
        vector<int> edge_degree;
        for(int i=0;i<m;i++) edge_degree.push_back(Edge[i].nodes.size());
        sort(edge_degree.begin(),edge_degree.end(),greater<int>());

        cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
        cout<<"# p , k-1 , partition time , total time , shield degree , shield per "<<endl; 
        int rec_s = -1;
        vector<double> candidate;
        for(int j=2;j<=5;j++) candidate.push_back(0.1*j);
        int p = 16;

        // for(int p=2; p<=64;p*=2){
            // double tmp = 0.11*m;
            // double fac = pow(tmp,1.0/20);
            // cerr<<"fac:"<<fac<<endl;
            // for(double j = 0.1; int(j*m)!=0; j/=fac){
            for(auto &j:candidate){
                int sheild_heavy_node = edge_degree[int(j*m)];
                // if(rec_s == sheild_heavy_node) continue;
                // rec_s = sheild_heavy_node;
                solve(n,m,path,p,j);
            }
        // }
        cout<<endl;
        delete []Node;
        delete []Edge;
    }
}

void load_dataset(){
   // nn.push_back( 4566 );
    // mm.push_back( 4131 );
    // filename.push_back( "wiki_new.txt" );

    // nn.push_back( 4131 );
    // mm.push_back( 4566 );
    // filename.push_back( "wiki_new.txt-swap.txt" );

    // nn.push_back( 172091 );
    // mm.push_back( 53407 );
    // filename.push_back( "out.dbpedia-location" );

    // nn.push_back( 53407 ); //use
    // mm.push_back( 172091 );
    // filename.push_back( "out.dbpedia-location-swap.txt" );

    nn.push_back( 56519 );
    mm.push_back( 120867 );
    filename.push_back( "out.github" );

    nn.push_back( 120867 );
    mm.push_back( 56519 );
    filename.push_back( "out.github-swap.txt" );

    nn.push_back( 127823 );
    mm.push_back( 383640 );
    filename.push_back( "out.actor-movie" );

    nn.push_back( 383640 ); // use
    mm.push_back( 127823 );
    filename.push_back( "out.actor-movie-swap.txt" );

    // nn.push_back( 901166 );
    // mm.push_back( 34461 );
    // filename.push_back( "out.dbpedia-team" );

    // nn.push_back( 34461 ); //use
    // mm.push_back( 901166 );
    // filename.push_back( "out.dbpedia-team-swap.txt" );

    nn.push_back( 1953085 );// use
    mm.push_back( 5624219 );
    filename.push_back( "out.dblp-author" );

    nn.push_back( 5623931 );
    mm.push_back( 1953085 );
    filename.push_back( "out.dblp-author-swap.txt" );

    nn.push_back( 781265  );// use
    mm.push_back( 283911   );
    filename.push_back( "reuters.txt" );

    nn.push_back( 283911 );
    mm.push_back( 781265 );
    filename.push_back( "reuters-swap.txt" );

    nn.push_back( 27665730 );
    mm.push_back( 12756244 );
    filename.push_back( "out.trackers" );

    nn.push_back( 12756244 );
    mm.push_back( 27665730 );
    filename.push_back( "out.trackers-swap.txt" );

    nn.push_back( 2783196 );
    mm.push_back( 8730857 );
    filename.push_back( "out.orkut-groupmemberships" );

    nn.push_back( 8730857 );
    mm.push_back( 2783196 );
    filename.push_back( "out.orkut-groupmemberships-swap.txt" );

    nn.push_back( 8116897  );
    mm.push_back( 42640545 );
    filename.push_back( "enwiki.txt" );

    nn.push_back( 42640545 );
    mm.push_back( 8116897  );
    filename.push_back( "enwiki-swap.txt" );

}

int main(int argc,char *argv[]){
    string method;
    method = argv[1];
    // method = "basic";
    cerr<<method<<endl;
    load_dataset();
    // unit_single();
    // unit_basic();
    // unit_entropy();
    // cout<<"# dataset:"<<path<<" n:"<<n<<" m:"<<m<<" sheild degree:"<<edge_degree[int(0.01*m)]<<endl;
    // cout<<"# p , k-1 , partition time , total time "<<endl; 
    // for(int i=2;i<=64;i*=2){
    get_partition_result(method);
    // }
    // sheild_select();


    return 0;
}