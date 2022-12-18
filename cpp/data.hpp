#pragma once
#include <bits/stdc++.h>
// #include "buffer.hpp"
// #include "k_core.hpp"
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
    unordered_map<int,int> rest;
    void reset(){
        rest.clear();
        for(auto &n_id:nodes) rest[n_id] = 1;
    };
    void erase(int n_id){
        rest.erase(n_id);
    }
};
