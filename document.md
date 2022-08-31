# Document 
## data.py
提供数据预处理/读取操作

### 接口列表:
```python
def preprocess_raw_data(shuffle = True): # 将link.csv的数据处理为超图流式数据,存放在./data/vertex_stream.txt中
# return: None
# shuffle: 是否打乱节点顺序,默认打乱

def vertex_stream(): #流节点迭代器,实例化后每次使用next获得下一个节点数据
# return: (node_id,degree,[edge_id]),若流读取完后一致返回None,None,None



```

## partition.py
分区算法
### 接口列表
```python
def hypergraph_information():# 将数据流一次获得超边:超边包含的节点
# return: 超边id:[超边包含的节点]

def cal_cost(node,core_edge,edge_degree):# 计算给定节点加入core_edge的代价
# return: 对应的代价

def random_core_set(node_list,core_size,edge_degree): # 对于给定节点序列,以及生成core_size的大小,随机生成core_set,需要使用超边度数作为代价计算的依据
# return: (core_node,core_edge) 核心集顶点列表[],定点集超边字典{}
```