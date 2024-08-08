# RAG

<img src="resources\simple_rag_workflow.png" width="80%">


## Knowledge Process & Storage


## Retrival


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

