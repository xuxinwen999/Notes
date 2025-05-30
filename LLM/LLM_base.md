# LLM模型基础


## 数据
### 通用语料
数据质量提升至关重要，甚至在scalingl law的研究中，增加dataset size的前提是保证数据质量。
* crawled pages处理：提取url中的文本信息，丢弃其中无用的广告、标题、目录等，工具如trafilatura等
* 语言过滤：使用 tool(ex. fastText) 训练一个语言识别模型，过滤目标语言得分低于threshold的docs
* 低质量过滤：通用语料低质量定义包括:
    - 内容重复（和deduplication有区别）
    - 文档或句子长度过短 
    - 纯数字、纯标点字符等，或标点占比过大
    - 广告？
* Deduplication
### 领域语料


## [Tokenization](https://huggingface.co/docs/transformers/en/tokenizer_summary)
* **Space and punctuation / rule-based tokenization (SpaCy/Moses)**: 生成vocab太大，比如 Transformer XL的vocab size高达200+K，而transformer结构模型的vocab size一般应在[50K以下，单语言更小。](https://huggingface.co/docs/transformers/en/tokenizer_summary)
* **BPE**: 从一个base vocab出发，训练过程迭代合并frequecy高的co-occurrence sub-string，终止条件为vocab size（hyperparameter）。其中，base vocab生成方法：
    - Unicode character: 字符太多导致base vocab太大，并且合并生成的string也会很多；训练过程费时；要考虑不同语言的字符合并问题等等；
    - Byte-base: GPT-2提出使用，先将text char用UTF-8编码，再在bytes基础上进行BPE merging.
* **WordPiece**: 核心和BPE一样是greedy merge, criterion有区别，BPE是基于统计的frequency, 而WordPiece是基于min negative likelihood(loss)。（两者导致的resulting vocab区别待看）
* **Unigram Model**: 从一个超大的sub-string vocab（通常包括training dataset所有的str）开始，每次迭代去掉一定比例使loss增长最少的str，终止条件仍然是vocab size
* **SentencePiece**: google一个开源项目，集成BPE和Unigram两种训练方法，增加了一下tricks(如space替换方案)以处理不同语言和scripts


## Embedding
### Token Embedding
* **Embedding Model**
    * 模型结构：enc+dec、
    * 预训练：BERT pretraining paradigm
    * finetune: 
        - 对比学习：构建高质量负样例、难负样例（虽然bce技术报告说太难的负样例会干扰模型训练），neg数量应多很多
        - instruction following
    * 下游任务多样性：构建通用的embedding模型
        - clustering, 
        - Info Retrieve：
            1. Dense: text -> vector, 取[cls], 计算向量相似度cos
            2. Sparse: term -> vector, 每个term(token)取最后一个hidden state 对应位置的向量 * 映射矩阵M得到该term的权重向量vector，计算cos实现关键词级别的匹配检索
            3. Multi-Vector：取整个序列的hidden state做计算，细节看bge-m3 report
    * 语料：title-body, title-abstract, instruction-output
### Position Embedding
* **Transformer结构的位置编码：[基础](https://zhuanlan.zhihu.com/p/454482273)**<br>
    **理想编码函数**至少满足：bijective、有界、连续、线性（能正确反映出相对位置关系）、可外推。
    * ***int编码***：高度依赖位置数值；无法外推（推理过程中遇见比训练序列长度更长的序列无法处理）。
    * ***[0,1]范围编码***：依然依赖位置数值，表示不同长度的序列时，token间距不一致。
    * ***二进制编码***：离散空间，同一序列的token间距都不相等。
    * ***sin函数***（频率是维度i的函数）：不是t的线性函数，无法正确反映相对位置关系。
    * ***正余弦成对编码***（[Attention Is All You Need](https://arxiv.org/pdf/1706.03762)）: 向量维度除2，从i=0开始两两成对，每组共享频率，则不同位置t可以通过线性变换得到，以此反映序列中相对位置关系。**重要性质**（[ref: 公式推导分析](https://arxiv.org/pdf/1911.04474)）：
        1) 不同位置的编码差异主要体现在靠前的维度上（*思考*：所以高维位置编码的意义不大？）
        2) 两个位置编码的点积仅与这两个位置的相对距离有关（*思考*：所以位置编码直接加在emb上去计算attention是有意义的，能有效引入两个token之间的相对位置关系 -> 不对，见性质4 ）
        3) 位置编码的点积是无向的：也就是token t 和 t-k、t+k两个位置的点积相等，仅与k有关。
        4) 进入attention计算后（乘上Q/K权重矩阵后），位置编码点积关于相对位置k的0轴对称性被破坏 -> 这种编码方式不能在transformer-based的模型中正确表达相对位置关系。
    * ***相对位置编码***：由于上述第四条性质，后续产生了一系列相对位置编码的工作，主要体现在计算context token ${t}_{m}$ 和 target token ${t}_{n}$ 的attention score时，引入一些trainable或functional的adding terms，以引入${t}_{m}$ 和 ${t}_{n}$ 的相对位置信息, 核心idea还是遵循adding PE的想法。
    * ***RoPE***：<br>
        **【主要特点】**：
        1) 在${W}_{q}$和${W}_{k}$后再融入位置信息；
        2) 位置信息以乘上旋转矩阵的方式参与attention，而不是（[Transformer](https://arxiv.org/pdf/1706.03762)）中在embedding上加上等维位置编码；
        3) 乘旋转矩阵可以在每个block和layer上保证位置信息的有效性，而Transformer的位置编码方式却可能导致位置信息随网络加深而减弱；
        4) 高维旋转（dim维）其实是在$dim/2$个子空间上做多次二维旋转，每个子空间有独立的基础旋转角度，而这个基础旋转角度的定义决定了不同位置$t$的位置信息区别在低维空间更明显，也就是越靠前的维度差异越大。
        5) RoPE还具备远程衰减性：即内积与相对距离反相关。符合语言特点。
        <br> 更多性质分析见[位置编码视频](https://www.bilibili.com/video/BV1Xi421R7ev/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=cf2e31ac835b0b0ad63aebcc493a3ebf)
        <br>
        [**ROPE适应推理长度增加的策略简介**](https://zhuanlan.zhihu.com/p/670280576)
### Why adding?
<img src="resources\emb_adding.png" width="60%">

## GPU requirements analysis
模型参数量单位B和显存单位GB之间存在的联系：1 GB = 1 B bytes, 而相关参数存储类型fp32 (4 bytes) / fp16 (2bytes)。<br>
分析显存占用主要从以下方面：
* Parameters：主要看参数数据类型，参考上述方式计算；(**inference**)
* Activations: 与batch_size和seq_length相关；(**inference**)
* Gradients: same with parameters;
* Optimizer States: 
* KV Cache: 2 × dim × Layers × Batch_Size × Sequence_Length × sizeof(float)
* Communication Buffers (Model Parallelism)
* Pipeline Buffers (Pipeline Parallelism)


## Model Architecture
* Attention进化：
    1. multi-head attention. 为了reduce memory bandwidth from loading
        keys and values, 对多个 K,v 做mean pool实现MQA: <br>
    <img src="resources\k_mean_pool.png" width="60%">
    2. multi-query attention. 但是这样对larger model不公平，为了keep the same proportional
        decrease in bandwidth and capacity as model size increases，对 attention 进行分组操作，query 被分为 N 组(超参)，每个组共享一个 Key 和 Value 矩阵实现GQA.
    3. GQA <br>
    <img src="resources\attention进化.png" width="80%">



## Training
### 语料变长序列的batch training处理
* **Padding & Masking:** often token_id=0 or a special token like [PAD], then mask the padded tokens so that they do not contribute to the model's loss or computations (important for attention mechanisms, where padded tokens should be ignored). 在padding阶段需要一个batch max_length, 可以人为设置(可能需要truncate过长的句子)，或者采用dynamic, 即采用每个bacth中最长的序列length.
* **Bucketing Sequences:** 先把序列按长度分组以保证每组序列长度相差不大，可以有效减少padding浪费
* **拼接序列替代batch训练:** 用序列并行替代数据并行减少无效计算: [知乎讨论原帖](https://zhuanlan.zhihu.com/p/700491837)
### 并行策略
* Data Parallelism：each GPU holds a copy of the entire model and processes different batches of data.
* Model Parallelism： different parts of the model are distributed across multiple GPUs. This requires ***efficient communication*** between GPUs.
* Pipeline Parallelism: dividing the model into stages, with each stage assigned to a different GPU. This also requires managing activations between stages.
### 训练框架：
* DeepSpeed
* Megatron-LM
### Training Tricks
* Scaling Law
Factors of model performance (cross-entropy loss) are currently considered as **{model size (N), dataset size (D), amount of training compute}**. 已发表的scaling laws:
    - **KM scaling law** (openai, 2020)
    - **Chinchilla scaling law** (deepmind, 2022)  
以上两者进行了不同角度的对照实验 (*原文待看*)，其中不同的观点包括算力固定时，如何对*N*和*D*进行scaling能更好提高模型表现，前者认为*N*占比更重，而后者认为均等。*注：仅从cross-entropy loss角度分析，不包括in-context learning能力。*  
* Given a fixed computing budget, training a larger model for fewer steps is better than training a smaller model for more steps （**?**） ([来源: HF](https://huggingface.co/blog/moe))


## Inference
### 参数说明
* **temperature**: temperature相当于对logits进行scale: logits=logits/temperature。 当temperature较高时，会更平均地分配概率给各个token，这导致生成的文本更具随机性和多样性；temperature较低接近0时，会倾向于选择概率最高的token，从而使生成的文本更加确定和集中。注：temperature=1时表示不使用此方式。
* **top-p**: It sets a threshold probability and selects the top tokens whose cumulative probability exceeds the threshold.
* **top-k**: It limits the model’s output to the top-k most probable tokens at each step.
* **batch inference**: When batching, you send multiple inputs through the model at once and get multiple outputs. 对单个序列只能in-sequence, 因为generation不像train那样有groud-truth可用。这种seq-batch work的原因主要是：1）节省了streaming the model's weights into registers的时间，一次load可用于多个input requests；2）充分利用sever算力.

##  LLM Capabilities
<img src="resources\llm_capab.png" width="100%">

#### Emergent Ability
" The abilities that are not present in small models but arise in large models ", 目前主要关注的通用大模型的涌现能力包括：
1. In-context learning
2. Instruction following
3. Step-by-step reasoning


## 评估
**Knowledge评估**: 在测试LLM对pure knowledge的掌握时，测试形式为多选项选择题，应警惕"educated guesses"问题。
### Benchmark
* **superCLUE-OPEN**
目前暂未开放数据集，社区评测模型结果基本基于OPEN数据（当然，据相关性分析报告，OPEN与OPT具有较高一致性，不过根据描述，测试点应该不同）：SuperCLUE-Open是一个多轮开放域中文基准，包括600个高质量多轮问题。这里面的问题用于评估中文大模型对话能力和遵循指令的能力。 里面包括一些常用的使用场景和一些挑战性的指令用于区分不同的模型。它考察模型的十大能力， 包括：语义理解与抽取，闲聊，上下文对话，角色扮演，知识与百科，生成与创作，代码，逻辑与推理，计算，代码和安全。每个子能力六十道题目，每个题目包括两轮问题。 
* **CMMLU**
CMMLU是一个综合性的中文评估基准，专门用于评估语言模型在中文语境下的知识和推理能力。CMMLU涵盖了从基础学科到高级专业水平的67个主题，包括12k选择题。它包括：需要计算和推理的自然科学，需要知识的人文科学和社会科学,以及需要生活常识的中国驾驶规则等。此外，CMMLU中的许多任务具有中国特定的答案，可能在其他地区或语言中并不普遍适用。（可作为通用能力的补充）
* **Xiezhi**
    全集总共约250k多选问答题，其中包括170k从各阶段考试题生成的问答多选题和80k从academc surveys中提取生成并回答+分类的多选问答题，涵盖的遥感相关学科分类如下：
        - "地球物理学": ["固体地球物理学", "空间物理学"],
        - "地理学": ["自然地理学","人文地理学","地图学与地理信息系统"],
        - "地质学": ["矿物学","岩石学","矿床学","地球化学","古生物学与地层学","古人类学","构造地质学","第四纪地质学"],
        - "大气科学": ["气象学","大气物理学与大气环境"]，
        - "地质资源与地质工程": ["矿产普查与勘探","地球探测与信息技术","地质工程"]，
        - "水利工程": ["水文学及水资源","水力学及河流动力学","水工结构工程","水利水电工程","港口、海岸及近海工程"],
        - "测绘科学与技术": ["大地测量学与测量工程","摄影测量与遥感","地图制图学与地理信息工程"],
        - "环境科学与工程": ["环境科学","环境工程"] <br>

    其中, *xiezhi-meta* 包括20k由chatgpt+人工确认的考研题生成，质量高；*xiezhi-specialty*和*interdiscipline*的区别是前者更独属于某个领域范围而后者更偏向应用多学科交叉知识解决，主要分开方法是按labels里面打的学科数多少，从noisy数据集中采样，相比meta可能质量偏低。

### METRICS
对每个多选题，options由1 answer+ 3 confusions (high relevant)+ 46 non-relevant, 被测LLM会根据生成概率对这50个opts排序，最后由MRR可视化：[0,1]之间，越大代表正确答案在LLM给出的排序中越靠前

### 值得注意的实验结论
小参数模型（6/7B）在学习领域知识的时候，会牺牲通用能力，we must do a trade-off


## Domain specific LLM
LLM掌握领域的factual knowledge应该包括以下能力：
* 记住facts
* 甄别基于facts的true/false statements
* Extend this definition to a whole knowledge base, not just a single fact.
### Training Tricks
continuing learning阶段应降低lr，以减小灾难遗忘