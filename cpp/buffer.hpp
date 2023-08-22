#pragma once
#include <bits/stdc++.h>
using namespace std;
typedef pair<int,int> P; 
class Buffer{
    struct MinHeap{
        bool operator()(P a,P b){
            return a.first > b.first;
        }
    };
    static bool cmp(const P &a,const P &b){
        return a.first > b.first;
    }

public:
    int maxi_size;
    unordered_map<int,int> *eval;
    unordered_map<int,int> check;
    vector<P> heap;
    void add(int id){
        if(check.find(id) != check.end()) return;
        if(check.size() == maxi_size && heap[0].first >= (*eval)[id]) return;
        if(check.size() == maxi_size && heap[0].first <  (*eval)[id]){
            pop_heap(heap.begin(),heap.end(),cmp);
            int remove_id = heap.back().second;
            heap.pop_back();
            check.erase(remove_id);
        }
        heap.push_back(P((*eval)[id],id));
        push_heap(heap.begin(),heap.end(),cmp);
        check[id] = 1;
    }
    vector<int> get_topk(int k){
        priority_queue<P,vector<P>,MinHeap> topk;
        for(auto &item:check){
            int n_id = item.first;
            if(topk.size()<k){
                topk.push(P((*eval)[n_id],n_id));
                continue;
            }
            if(topk.size() == k && topk.top().first<(*eval)[n_id]){
                topk.pop();
                topk.push(P((*eval)[n_id],n_id));
            }
        }
        vector<int> ret;
        while(topk.size()!=0) {
            int id = topk.top().second;
            ret.push_back(id);
            topk.pop();
        }
        return ret;
    }
    Buffer(int m_size ,std::unordered_map<int,int> *E){
        this->eval = E;
        this->maxi_size = m_size;
    }
    void erase(int id){
        check.erase(id);
    }
    void rebuild(){
        heap.clear();
        heap.resize(check.size());
        int i = 0;
        for(auto &item:check) {
            int n_id = item.first;
            heap[i++] = P((*eval)[n_id],n_id);
        }
        make_heap(heap.begin(),heap.end());
    }
    bool exist(int id){
        return check.find(id) != check.end();
    } 
    int size(){
        return check.size();
    }
    void clear(){
        check.clear();
        heap.clear();
    }
    void build(vector<int> nodes){
        clear();
        vector<P> h;
        h.resize(nodes.size());
        int i =0;
        for(auto &n_id:nodes){
            h[i++] = P((*eval)[n_id],n_id);
        }
        make_heap(h.begin(),h.end());
        int size = min(maxi_size,int(nodes.size()));
        heap.resize(size);
        for(int i=0;i<size;i++){
            int n_id = h[i].second;
            heap[i] = h[i];
            check[n_id] = 1;
        }

    }
};
