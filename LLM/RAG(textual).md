# RAG: textual version
<img src="resources\retrievers.PNG" width="80%">
<img src="resources\simple_rag_workflow.png" width="80%">

## TODO LIST
* 需要学习的板块总结：https://mp.weixin.qq.com/s/g7qE2pOifIMj21W3qJFzNQ
* graphRAG:
    1. https://neo4j.com/blog/genai/graphrag-manifesto/


## Knowledge Process & Storage
### [Chunking](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb)
* **Character Splitting**: overlap应该主要应用于这个分割方式，以追溯word/phrase的完整性，后面基于保留句段完整性和语义的分割方式不应该采用fixed size overlap, 这样反而使chunk头尾不完整。
* **Recursive Character Text Splitting**: recurse对象应该是seperator list, 每次pop一个seperator分割文本，再检查每个chunk size，对超出size的chunk采用下一个seperator继续切分。
* **Code/HTML/Markdown**: 扩展一些适配script type的seperator，仍然是char-based seperator划分方法。
* **Semantic Chunking**：
    - 先完成sentence-based splitting
    - 设定一个buffer window (size n, 表示这个windown中包含2n+1个上述的sentences, 即当前句为中心句，前后各组合n句), 对每个window计算cos similarity, 窗口每次滑动一个sentence再次计算cos similarity，得到每个中心句的cosine表示。（以window组合计算中心句的cos可以降低噪声，链接原文提到的）。
    - 基于percentile选定划分点，这样做是站在全篇doc的语义基础上进行相对划分，更合理。


## Information Retrieval
The **goal** of an IR system is not just to **return a list of documents** but to ensure that **the most relevant ones appear at the top** of the results.
### Statistical Methods
Based on term frequency and document relevance, these methods are efficient and effective for keyword-based search but often struggle with understanding the deeper context or semantics of the text.
* TF-IDF
* BM25
    1. **ElasticSearch BM25**: Best Match 25(25没有实际意义，可以看作版本名)，改进TF-IDF算法，增加了几个可调节的参数，使其在应用中更具灵活性和实用性，并对计算进行更合理的定义和限制。下图是输入query Q与文档D的bm25分数计算解析：<br>
<img src="resources\es_bm25.png" width="60%"><br>
ES为文档创建json，包含content, author, title等field，可以在field上指定创建index：对text创建Inverted index是指用分词器分词->创建term-doc index<br>
([ES简介](https://mp.weixin.qq.com/s/wlh2AHpNLrz9dHxPw9UrkQ))

### Semantic Modeling (Vector Retrieval)
#### 索引字段
* Dense vector: normal emb 模型对分片文本的整段编码（[cls] or mean-pooling），编码含义与emb模型训练任务相关；
* Sparse vector: 表示为不定维度的position-value pair {position: value}，维度和匹配到vocab的关键词相关；
#### 向量检索方法
（待整理）[REF: 以阿里云OpenSearch为例谈向量检索技术选型 - <em>阿里云</em>开发者的文章 - 知乎](https://zhuanlan.zhihu.com/p/657531099)
### retrieve efficacy eval
* Precision: 尽量避免返回无关内容
* Recall: 尽量召回更多相关内容
* Ranking: 召回内容相关性排序








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

