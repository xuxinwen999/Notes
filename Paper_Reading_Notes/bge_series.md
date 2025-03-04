## BGE M3-Embedding

### Features
* **multi-linguality**: support more than 100 world languages byy learning a common semantic space for different languages.
* **support different retrieval functionalities**: dense retrieval, sparse retrieval and multi-vector retrieval.
* **up to 8192 input tokens**

### Data Curation
* Pre-training Stage: generated from unsupervised multi-lingual corpora,
    1. extracting the rich-semantic structures, e.g., title-body, title-abstract, instruction-output;
    2. To learn the unified embedding space for cross-lingual semantic matching, the parallel sentences are introduced from two translation datasets.
* Fine-tuning Stage: labelled dataset and synthetic data. Synthetic data由prompt+GPT3.5生成，旨在 mitigate the shortage of long document retrieval tasks and
introduce extra multi-lingual fine-tuning data, 格式为从given paragraphs中生成合适的questions.

###  Three Common Retrieval Functionalities
对最后一层的hidden states ${H}_{q}$
* Dense Retrieval: 以位于P0的[cls]为seq representation, 输出$norm({H}_{q})$计算cosine similarity；
* Sparse Retrieval: 对每个tokenized term，计算其$ weight=relu({W}^{T}_{lex}{H}_{q}) $, 其中$ {W}^{T}_{lex} $是learnable matrix. 同一seq中多次出现的term取max weight. 计算query和passage相似度是取两个seq共有的terms进行相应的weights内积计算；
* Multi-Vector Retrieval： 依然引入一个learnable matrix, [cls]不参与计算，仅取passage中最大weight term, 具体看原文(懒得写了)<br>

**Notes:** 该工作中对多路召回结果融合采取scores相加

### Training Settings
* Architecture: XLM-RoBERTa model ([跨语言预训练模型XLM(R)介绍](https://zhuanlan.zhihu.com/p/620505640)) pre-trained further through the *RetroMAE(待看)* method.
* Pre-train Stage: only the dense retrieval is trained in the basic form of contrastive learning
* 