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

    n = 56520;
    m = 120870;
    string path = "../data/github/github.txt";

    Node = new HyperNode[n];
    Edge = new HyperEdge[m];
    for(int i=0;i<n;i++) Node[i].id = i;
    for(int i=0;i<m;i++) Edge[i].id = i;
    load_data(path,Node,Edge);

    for(int i=2; i<20; i++){
        int p = 16;
        int topk = 50;
        int buffer_fac = 10;
        bool set_kcore = false;
        int shield_heavy_node = i*10;
        solve(n,m,Node,Edge,p,topk,buffer_fac,set_kcore,shield_heavy_node);
    }

    return 0;
}
