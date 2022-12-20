#include <bits/stdc++.h>
using namespace std;
int main(){
    int maxi = 5e5;
    int query = 5;
    int cnt = 0;

    clock_t beg = clock();
    unordered_map<int,int> mp;
    for(int i=0;i<maxi;i++) mp[i] = 1;
    for(int i=0;i<maxi;i++){
        mp.erase(i);
        int rd = rand()%maxi;
        for(int j=0;j<query;j++)
            if(mp.find(rd)!=mp.end()) cnt++;
    }
    cerr<<(clock()-beg)*1000/CLOCKS_PER_SEC<<endl;

    beg = clock();
    unordered_set<int> st;
    for(int i=0;i<maxi;i++) st.insert(i);
    for(int i=0;i<maxi;i++){
        st.erase(i);
        int rd = rand()%maxi;
        for(int j=0;j<query;j++)
            if(st.find(rd)!=st.end()) cnt++;
    }
    cerr<<(clock()-beg)*1000/CLOCKS_PER_SEC<<endl;


}