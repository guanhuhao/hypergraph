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
};
