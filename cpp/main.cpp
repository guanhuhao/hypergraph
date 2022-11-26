#include <bits/stdc++.h>
using namespace std;
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
HyperNode *Node;
HyperEdge *Edge;
void load_node(string path){
    unordered_map<int,HyperNode> mp_node;
    FILE *file;
    file = fopen(path.c_str(),"r");
    int n_id,e_id;
    while(fscanf(file,"%d%d",&n_id,&e_id)){

    }
}
// void load_edge(string path){

// }
int main(){
    // string path = "../data/github/github.txt"
    string path = "../data/wiki/wiki.txt";
    load_node(path);
    return 0;
}
