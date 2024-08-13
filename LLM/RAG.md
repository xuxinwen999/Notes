# RAG

<img src="resources\simple_rag_workflow.png" width="80%">


## Knowledge Process & Storage


## Retrieval
### retrieve efficacy eval
* Precision: 尽量避免返回无关内容
* Recall: 尽量召回更多相关内容
* Ranking: 召回内容相关性排序
<img src="resources\retrievers.PNG" width="80%">

### Vector Retrieval
* Dense vector: normal emb 模型对分片文本的整段编码（[cls] or mean-pooling），编码含义与emb模型训练任务相关；
* Sparse vector: 表示为不定维度的position-value pair {position: value}，维度和匹配到vocab的关键词相关；

### Key-word / Full-text Retrieval
* **ElasticSearch BM25**: Best Match 25(25没有实际意义，可以看作版本名)，改进TF-IDF算法，增加了几个可调节的参数，使其在应用中更具灵活性和实用性，并对计算进行更合理的定义和限制。下图是输入query Q与文档D的bm25分数计算解析：<br>
<img src="resources\es_bm25.png" width="60%"><br>
ES为文档创建json，包含content, author, title等field，可以在field上指定创建index：对text创建Inverted index是指用分词器分词->创建term-doc index<br>
[ES简介](https://mp.weixin.qq.com/s/wlh2AHpNLrz9dHxPw9UrkQ)





## Generation


## Tools and Frameworks

### LlamaIndex

* Metadata: additional information can be included to help inform responses and track down sources for query responses
    - llamaindex默认的metadata是json格式，连接到向量库时，应遵循向量库的格式要求，如str等；
    - Any information set in the **metadata** dictionary of **each document** will **show up in** the metadata of each **chunk node** created from the document;
    - enabling the index to utilize it on queries and responses;
    - By default, the **metadata** is injected into the text for both **embedding** and **LLM model calls**
    - [Customize metadata](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_documents/#customizing-metadata-format): 可以限定embedding和llm模型接收的metadata字段、定制metadata和chunk_text join的模板


## 思考
* 未来portable llm applications是否可以向提炼强推理的small size llm（舍弃一些memory参数） + 外挂RAG的paradigm发展？

### ReRanker
bge-reranker的介绍是在pretrained的bert模型上做监督微调 (text-paris数据，label is binary that indicates the similarity of the pair)

