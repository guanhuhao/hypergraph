#include <bits/stdc++.h>
using namespace std;
int main(){
    int maxi = 5e5;
    int query = 5;
    int cnt = 0;

    clock_t beg = clock();
    unordered_map<int,bool> mp;
    for(int i=0;i<maxi;i++) mp[i] = true;
    for(int i=0;i<maxi;i++){
        mp[i] = false;
        for(int j=0;j<query;j++){
            int id = rand()%maxi;
            if(mp[id] == true){
                cnt += 1;
            }
        }
    }
    clock_t end = clock();
    cerr<<"unordered map runtime:"<<(end-beg)*1000/CLOCKS_PER_SEC<<"ms"<<endl;

    beg = clock();
    set<int> st;
    for(int i=0;i<maxi;i++) st.insert(i);
    for(int i=0;i<maxi;i++){
        st.erase(i);
        for(int j=0;j<query;j++){
            int id = rand()%maxi;
            if(st.find(id) != st.end()){
                cnt += 1;
            }
        }
    }
    end = clock();
    cerr<<"set runtime:"<<(end-beg)*1000/CLOCKS_PER_SEC<<"ms"<<endl;


}