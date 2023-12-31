## 数据处理
#### 通用预料
数据质量提升至关重要，甚至在scalingl law的研究中，增加dataset size的前提是保证数据质量。
1. crawled pages处理：提取url中的文本信息，丢弃其中无用的广告、标题、目录等，工具如trafilatura等
2. 语言过滤：使用 tool(ex. fastText) 训练一个语言识别模型，过滤目标语言得分低于threshold的docs
3. 低质量过滤：通用语料低质量定义包括:
    - 内容重复（和deduplication有区别）
    - 文档或句子长度过短 
    - 纯数字、纯标点字符等，或标点占比过大
    - 广告？
4. Deduplication

#### 领域语料


## Training Tricks
#### Scaling Law
Factors of model performance (cross-entropy loss) are currently considered as **{model size (N), dataset size (D), amount of training compute}**. 已发表的scaling laws:
- **KM scaling law** (openai, 2020)
- **Chinchilla scaling law** (deepmind, 2022)  
以上两者进行了不同角度的对照实验 (*原文待看*)，其中不同的观点包括算力固定时，如何对*N*和*D*进行scaling能更好提高模型表现，前者认为*N*占比更重，而后者认为均等。*注：仅从cross-entropy loss角度分析，不包括in-context learning能力。*  

#### Parallel Training
训练框架：
- DeepSpeed
- Megatron-LM


## Emergent Ability
" The abilities that
are not present in small models but arise in large models ", 目前主要关注的通用大模型的涌现能力包括：
1. In-context learning
2. Instruction following
3. Step-by-step reasoning


## 评估
predictable scaling (GPT-4)：

### Benchmark
#### superCLUE-OPEN
目前暂未开放数据集，社区评测模型结果基本基于OPEN数据（当然，据相关性分析报告，OPEN与OPT具有较高一致性，不过根据描述，测试点应该不同）：SuperCLUE-Open是一个多轮开放域中文基准，包括600个高质量多轮问题。这里面的问题用于评估中文大模型对话能力和遵循指令的能力。 里面包括一些常用的使用场景和一些挑战性的指令用于区分不同的模型。它考察模型的十大能力， 包括：语义理解与抽取，闲聊，上下文对话，角色扮演，知识与百科，生成与创作，代码，逻辑与推理，计算，代码和安全。每个子能力六十道题目，每个题目包括两轮问题。 

#### CMMLU
CMMLU是一个综合性的中文评估基准，专门用于评估语言模型在中文语境下的知识和推理能力。CMMLU涵盖了从基础学科到高级专业水平的67个主题，包括12k选择题。它包括：需要计算和推理的自然科学，需要知识的人文科学和社会科学,以及需要生活常识的中国驾驶规则等。此外，CMMLU中的许多任务具有中国特定的答案，可能在其他地区或语言中并不普遍适用。（可作为通用能力的补充）

#### Xiezhi
全集总共约250k多选问答题，其中包括170k从各阶段考试题生成的问答多选题和80k从academc surveys中提取生成并回答+分类的多选问答题，涵盖的遥感相关学科分类如下：
- "地球物理学": ["固体地球物理学", "空间物理学"],
- "地理学": ["自然地理学","人文地理学","地图学与地理信息系统"],
- "地质学": ["矿物学","岩石学","矿床学","地球化学","古生物学与地层学","古人类学","构造地质学","第四纪地质学"],
- "大气科学": ["气象学","大气物理学与大气环境"]，
- "地质资源与地质工程": ["矿产普查与勘探","地球探测与信息技术","地质工程"]，
- "水利工程": ["水文学及水资源","水力学及河流动力学","水工结构工程","水利水电工程","港口、海岸及近海工程"],
- "测绘科学与技术": ["大地测量学与测量工程","摄影测量与遥感","地图制图学与地理信息工程"],
- "环境科学与工程": ["环境科学","环境工程"]  

其中,  
1. *xiezhi-meta* 包括20k由chatgpt+人工确认的考研题生成，质量高；
2. *xiezhi-specialty*和*interdiscipline*的区别是前者更独属于某个领域范围而后者更偏向应用多学科交叉知识解决，主要分开方法是按labels里面打的学科数多少，从noisy数据集中采样，相比meta可能质量偏低。

**METRICS**: 对每个多选题，options由1 answer+ 3 confusions (high relevant)+ 46 non-relevant, 被测LLM会根据生成概率对这50个opts排序，最后由MRR可视化：[0,1]之间，越大代表正确答案在LLM给出的排序中越靠前

**值得注意的实验结论**：小参数模型（6/7B）在学习领域知识的时候，会牺牲通用能力，we must do a trade-off


## LLM Application
将LLM包装成一个工具作为solver，或是作为agent扮演controller的角色实施工具调用，是目前主要研究的两条路线。也有一些给工作在有限计算资源解决特定下游任务时，寻求两条路线的一个中间状态，将LLM结合一些plugin, 如调用calculator完成计算 (由于自然语言表述数学表达式的局限性，LLM在计算方面能力较为欠缺)、调用搜索引擎抓取up-to-date信息以生成更好的回答(预训练数据通常没有实时性)