# LLM-based Agent

将LLM包装成一个工具作为solver，或是作为agent扮演controller的角色实施工具调用，是目前主要研究的两条路线。也有一些给工作在有限计算资源解决特定下游任务时，寻求两条路线的一个中间状态，将LLM结合一些plugin, 如调用calculator完成计算 (由于自然语言表述数学表达式的局限性，LLM在计算方面能力较为欠缺)、调用搜索引擎抓取up-to-date信息以生成更好的回答(预训练数据通常没有实时性)


### ReAct
* Prompt Template (to LLM): [Quesion->[Thought->Action->Observation]](few-shot) -> Question: <br> 在领域应用中主要微调few-shot
* Function calling: LLM支持的function calling主要应用于调用tools时将LLM输出的actions自然语言转换为tool API接口参数格式和接口返回内容的自然语言改写。


### Function Calling & Tools
* Function Signature: 即function描述，includes the function name, parameters, and the expected return type. This is usually defined in a structured format (e.g., JSON).
* LLM FT (Training) goals towards function calling：
    - Recognize when a query matches a function’s use case；
    - Generate a call to the appropriate function with the correct parameters；
    - Integrates API results into its response.
* Error Handling: Managing errors or unexpected results from function calls.
* **QA**：
    - 多个function的signature会大大增加prompt长度，如何管理？
    - 如何考虑对API说明pre-process, 如int -> number
    - structure outputs: 填充complex multiple hierarchy json, 复杂func和拆解的简单func组合在效果上有什么区别？如下图：<br>
    <img src="resources\agent-0.png" width="60%">