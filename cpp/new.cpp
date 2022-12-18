#include <bits/stdc++.h>
#include "data.h"
#include "partition.hpp"
using namespace std;
int n,m;
HyperNode *Node;
HyperEdge *Edge;
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

    // n = 172080;
    // m = 53408;
    // string path = "../data/dbpedia-location/out.dbpedia-location";
    
    // n = 1953086;
    // m = 5624220;
    // string path = "../data/dblp-author/out.dblp-author";



    Node = new HyperNode[n]; 
    Edge = new HyperEdge[m];
    for(int i=0;i<n;i++) Node[i].id = i;
    for(int i=0;i<m;i++) Edge[i].id = i;
    load_data(path,Node,Edge);

    for(int i=2; i<64; i*=2){
        int p = i;
        int topk = 50;
        int buffer_fac = 10;
        bool set_kcore = false;
        int shield_heavy_node = 200;
        solve(n,m,Node,Edge,p,topk,buffer_fac,set_kcore,shield_heavy_node);
    }

    return 0;
}
