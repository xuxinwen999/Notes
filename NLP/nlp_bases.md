# NLP基础
* [NLP主流模型的前世今生简介](https://mp.weixin.qq.com/s/BxpWFwXFbpur_gTuzSEsSA)
* [NLP主流模型的前世今生详细版](https://mp.weixin.qq.com/s/R45FqZ8JMzFLkEz6LymNOg)
* BERT概括总结：BERT不是预测序列中的下一个词，而是被训练预测句子中random-masked tokens。这迫使模型在进行预测时考虑整个句子的上下文 — — 包括前后词语。下一句预测（Next Sentence Prediction — NSP）：除了MLM之外，BERT还接受了称为下一句预测的次要任务训练，其中模型学习预测两个句子是否在文档中连续。这帮助BERT在需要理解句子之间关系的任务中表现出色，例如问答和自然语言推理。通过生成深层次的、上下文丰富的文本表示，BERT在文本分类、命名实体识别（NER）、情感分析等**语言理解任务**中表现出色。
* GPT概括总结：初版GPT使用因果语言建模目标进行训练，其中模型仅基于前面的标记预测下一个标记。这使得它特别适合于生成任务，如文本补全、摘要生成和对话生成。同时，其并未损失在语言理解类任务上的表现，GPT的一个关键贡献是它能够在不需要特定任务架构的情况下针对特定下游任务进行微调。只需添加一个分类头或修改输入格式，GPT就可以适应诸如情感分析、机器翻译和问答等任务。而GPT2开始，随着参数量和训练数据量增加，GPT表现出zero-shot和few-shot的良好能力意味着它可以在没有任何特定任务微调的情况下执行任务。

## Loss Functions
* Categorical **Cross-Entropy Loss**: used for multiclass classification problems(for binary-classification, it's one-hot labelled). It measures the performance of a classification model whose output is a probability distribution over multiple classes:
<img src="resources\CEloss.png" width="100%">
*注：perplexity建立在CELoss上*

* **Contrastive Loss**: 相似性学习任务，learn embeddings such that similar items are closer in the embedding space while dissimilar items are farther apart. 输出标签通常是one-hot:
<img src="resources\contrasloss.png" width="80%">

* **KL loss**: 衡量两个分布的相似性，常用于模型蒸馏等。注意KL散度不具备对称性。
<img src="resources\KL.png" width="50%">

* **KL vs. CE**: 由于CE比KL多一个真实分布P的entropy, 所以当真实分布并不确定时，需要显化KL去做拟合。
<img src="resources\kl和ce.png" width="100%">

**为什么交叉熵更常用？**
1. 实现简洁性：框架内置的CrossEntropyLoss直接封装了log_softmax + NLLLoss，用户无需手动处理对数变换。KL散度需显式确保输入为对数概率（如调用log_softmax），容易因实现错误导致数值不稳定。
2. 数值稳定性：交叉熵的实现通常对数值问题（如log(0)）有更好的鲁棒性。
3. 任务适配性：分类任务中99%的场景使用one-hot标签，此时CE与KL等价，但CE更直观。

## Metrics
* Perplexity: it quantifies how well the model predicts the next word in a sequence. Lower perplexity indicates that the model is more confident and better at predicting the text. Commonly used in evaluating the performance of language models during training.
* BLEU compares the generated text (candidate) to one or more reference texts (human translations) by measuring the overlap of n-grams. BLEU scores range from 0 to 1, where a higher score indicates better quality. BLEU is primarily used in machine translation evaluation, assessing how closely machine-generated text matches human translations.