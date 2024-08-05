# [REAC T: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS](https://arxiv.org/pdf/2210.03629)
ReAct = Reasoning + Actions, 本文对LLM的COT Prompts还依赖few-shots
<img src="resouorces\react_00.png" alt="Comparison of 4 prompting methods" style="width: 80%; display: block; margin: auto;"></a>

## Main Works:
* Introduce ReAct, a novel ***prompt-based*** paradigm to ***synergize reasoning and acting*** in language models for general task solving；
* 在benchmarks上对比了react和纯reasoning/action gen的结果；
* 进行一些ablations分析acting在reasoning tasks的重要性，以及reasoning在interactive tasks中的重要性；
* 探索react在prompting setup下的一些limitations；
* react对在additional数据上进行ft的作用；
* react结合其他，如RL，进一步解锁llm的能力。

## Details
* 在原始的action集合上并入L集合：action_L refers to a thought or a reasoning trace:  decision making and reasoning capabilities are integrated into a large language model