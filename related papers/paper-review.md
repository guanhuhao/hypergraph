<!-- vscode-markdown-toc -->

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --> 

# Paper Review
## 2017-NIPS-Inhomogeneous Hypergraph Clustering with Applications
### 摘要概要:
1.超图分区在机器学习,计算机视觉,网络分析中有重要应用
2.基于最小化跨分区成本的标准化代价(normalized cost)忽略了同一超边中子集结构重要性(超边内存在更小的结构)
3.提出一种技术,并证明当非均匀代价满足次模性质时,该方法是最优解的一个二次逼近策略.
3.实验证明这种非均匀分配策略在结构学习(structure learning of ranking),自空间分割(subspace segmentation),模态聚类中有效.

### 想解决的问题
1.普通图分区(graph partition)无法考虑超边结构,同构超图分区(homogeneous)不考虑超边内结构

### 问题相关定义
1.采用点分区的方式来对超图进行分区
2.为了引入超边内不同结构的影响,对于构成超边$e$中的某种结构节点子集$\widetilde V$,使用评估函数$w_e(\widetilde V)$来量化表示
3.由于一个点可能存在多个超边中,且在不同超边中承担不同的作用,因此对于点$v$对于超边$e$的重要性使用评估函数$w_e(\{v\})$来表示,对于节点$v$对于整个超图的 **度数** $d_v$计为$\sum_{e\in E \& v\in e}w_e(\{v\})$,即所有包含节点$v$的超边$e$中节点单例集合${v}$的评估权重的和.
4.定义任意顶点集$S$的容量(volume)为该顶点集中所有顶点的度数和$vol(S) = \sum_{v\in S} d_v$(当分母用的),同时定义对于该顶点集的边缘集合(boundary set)$\partial S$定义为所有不完全包含在$S$中的边,同时计算分区$S$对于整体的代价:
$$
vol(\partial S) = \sum_{e\in \partial S} w_e(e\cap S)
$$
PS:实际上由于已经定义$w_e(\phi)=w_e(e)=0$,上式计算时可以不用区分$\partial S$
5.优化目标,对于k分区$S_1,S_2,...,S_k$优化目标定义为:
$$
NCut(S_1,S_2,...,S_k) = \sum_{i=1}^k\frac{vol(\partial S)}{vol(S_i)}
$$
PS:论文中(3)式计算单个分区$S$的代价,实际等效于2分区的情况

上述定义出自2000年一篇文章,详见原文参考文献[18] 

### 解决问题的方法
1&2.将超图映射为普通图,在映射阶段引入/添加超图约束
3.使用正则拉普拉斯矩阵进行谱聚类
4.将源问题转化为一个优化问题,并计算/提供一个可证明的最佳权值分割映射

### 评价方案的指标&实验效果

### 应用
网络模态聚类(network motif cluster):
> 真实网络存在丰富的高阶连接模式(high-order connectivity pattern),基于网络模态(Motif)的聚类可以学习网络高阶组成模式,相较于传统homogenous,inhomogenous引入超边内部关系可以更细粒度的解释这种高阶组成关系
