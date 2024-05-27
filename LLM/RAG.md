# RAG

<img src="resources\RAG_pipeline.jpg" width="80%">

### ReRanker
bge-reranker的介绍是在pretrained的bert模型上做监督微调 (text-paris数据，label is binary that indicates the similarity of the pair)


### Tools and Frameworks
- llamaindex
    * [loading and processing](https://docs.llamaindex.ai/en/stable/understanding/loading/loading/): processing包括chunking, extracting metadata, and embedding each chunk, 最好使用pipeline显式定义处理操作
