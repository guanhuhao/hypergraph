#include <bits/stdc++.h>
using namespace std;
int main(){
    string src,tar;
    int tot = 1;
    freopen("./links.tsv","r",stdin);
    map<string,int> mp;
    ofstream out("wiki.bi", ios::out | ios::binary);
    FILE *f_wtr = NULL;
    if((f_wtr = fopen("wiki.bi","wb")) == NULL)  {// w for write, b for binary
        cerr<<"open f_wtr file failed!"<<endl;
        return -1;
    }
    while(cin>>src>>tar){
        if(mp[src] == 0) {
            mp[src] = tot;
            tot++;
        }
        if(mp[tar] == 0) {
            mp[tar] = tot;
            tot++;
        }
       
        int u,v;
        u = mp[src]-1;
        v = mp[tar]+4600-1;
        fwrite(&u, sizeof(u), 1, f_wtr); 
        fwrite(&v, sizeof(v), 1, f_wtr); 
    } 
    cerr<<mp.size()<<endl;
}