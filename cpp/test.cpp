#include <bits/stdc++.h>
using namespace std;
int main(){
    int maxi = 5e5;
    int query = 5;
    int cnt = 0;

    clock_t beg = clock();
    unordered_map<int,int> mp;
    for(int i=0;i<maxi;i++) mp[i] = 1;
    for(int i=0;i<5;i++){
        for(auto &item:mp) cnt+= i*item.first;
    }
    cerr<<(clock()-beg)*1000/CLOCKS_PER_SEC<<endl;

    beg = clock();
    vector<int> v;
    for(int i=0;i<maxi;i++) v.push_back(i);
    for(int i=0;i<5;i++){
        for(auto &item:v) cnt+= i*item;
    }
    cerr<<(clock()-beg)*1000/CLOCKS_PER_SEC<<endl;


}