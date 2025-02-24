# Mixture of Experts Architecture
* Given a fixed computing budget, you can dramatically scale up the model or dataset size for training a MoE model than a dense counterpart model.
* Architecture: in MoEs we replace every FFN layer of the transformer model with an MoE layer, which is composed of a gate network and a certain number of experts.<br>
<img src="resources\moe_vs_transformer.png" width="70%">
<br>
    1. Sparse MoE layers 替换 FFNs (红框部分), 由多个experts组成, 可以是FFNs, more complex networks or even a MoE itself.
    2. A gate network or router, that determines which tokens are sent to which expert.
* FT阶段：有实验证明 (SF-MoE paper), updating MoE params while freezing others works bad,  但是反向操作, freezing MoEs效果不错: <br>
<img src="resources\07_superglue_bars.png" width="50%">
<br>
另外, sparse MoE models tend to benefit more from smaller batch sizes and higher learning rates.