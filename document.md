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


1.对于二维平面上确定激活的若干点的信息,使用确定的插值算法可以唯一确定其他所有点的值
2.对于两相邻的点,对于地图上其他点提供的信息增益是少的,因此应当尽可能分散的选择激活的点
3.对于两同向的点,对于地图上提供点提供的信息增益也是少的,因此应当选择方位差异较大的点激活
4.基于2,3可以对于地图上单点进行量化建模,计算已知点集对该点的信息量(建模考虑方位$\theta$与距离$dis$)
5.对于整体区域信息总量可以使用对地图上所有单点求和的方式计算
6.对于所有在预算限制下的备选方案可以找到对于整体区域信息总量最大的方案.
7.使用6得到的对整体区域信息总量最大的激活方案,计算其他点插值,并与真实值比较得到相对误差$D_1$
8.使用随机或者其他方式找到对应的激活方案,同样使用相同的插值算法计算其他点的插值,并同样计算相对误差$D_2$
9.实验证明$D_1<D_2$,说明该启发式的寻找激活方案是可行且优秀的
**PS:整个过程中所有点的真实值已知,但除7,8最后一步计算插值时不使用真实值作为建模依据**