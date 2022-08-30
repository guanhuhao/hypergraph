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
def hypergraph_information():# 将数据流一次获得统计信息
# return: dic超边度数字典
```