### Multi-level memory
仅针对单次请求(一个doc或一次翻译text)，未构建permanent memory
* **Long-term memory retrieve**: 维持一个max 20 sentences的上文窗口list[tuple(src, translation)], 提供few-shots。检索方式分为agent和embedding cosine
    - *agent*: prompt调模型
    - *embedding cosine*：原版调用'text-embedding-3-small'生成embeddings, query emb分别和context windows中的source emb计算cosine similarity后，在cosine上加上recency权重得到排序分数。
* **Short-term memory**: This component is specifically designed to capture immediate contextual information in adjacent sentences. 设置一个context window size, those then seamlessly integrated into the translation prompt, serving as the context for the current sentence.
* **Biligual summary**: 以固定数量的句子划分出paragraph, 每次产生新的paragraph时实施一个two-step process：
    1. 对单个paragraph做摘要，其中对src和tgt要求不同：
        - The Source-Side Summary encapsulates the main content domain, style, and tone of the previously translated sections of the document
        - Target-Side Summary focuses solely on the main content of the previously translated target text.
    2. merge summary to previous
This process is repeated iteratively until all sentences in the source document have been read.
* **Entity records**: 维护一个dict{src_ent: tgt_ent}保持一致性翻译。 对当前处理的sentence：
    - 提取dict中相关entities(或全部)加到翻译prompt；
    - 翻译结束后对src和hyp调模型做ner，将new ent和对应翻译(如无则保持原词)加入dict。对当前产生的冲突翻译有记录。
