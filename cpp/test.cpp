 
#include <bits/stdc++.h>
using namespace std;
int main(){
    unordered_map<int,int> mp;
    unordered_map<int,int> *p;
    p = &mp;
    mp[2] = 2;
    cerr<<(*p)[2]<<endl;

}