# 知识图谱、图数据库

## KG - Definitions
* 知识：每条知识表示为一个SPO三元组(Subject-Predicate-Object)

<img src="resources\SPO.png" width="40%">

* KG: (参考性定义) A knowledge graph consists of a set of interconnected typed entities and their attributes.


## Graph Database
<img src="resources\GB_vs_RB.png" width="80%">

[主流图数据库总览](https://db-engines.com/en/ranking/graph+dbms)


## KG implementions for Reasoning (AI)
* ***knowledge graph embeddings***: derives latent feature representations of entities and relations. ***GNN*** is trained to predict the value of a node embedding (provided a group of adjacent nodes and their edges) or edge (provided a pair of nodes), and then affords topology and data structures that provides a convenient domain for semi-supervised learning.
* Entity alignment: KG中一个问题方向。由于graph包含一定语境，同一entity可能在不同graph中出现。在解决实际问题时，现实世界中的subject如何与某个具体graph中的entity align是一个难题。上述以embedding编码graph在一定程度上缓解了这个问题。

