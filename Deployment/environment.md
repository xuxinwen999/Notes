### 问题解决
- ***issue***: -bash: /mnt/glusterfs/rscb/nlp/xxw/envs/qwen2/bin/ninja: /mnt/glusterfs101/rscb/nlp/xxw/envs/qwen/bin/python: bad interpreter: No such file or directory<br>
    ***solution***: 
    ```cli
    vim /mnt/glusterfs/rscb/nlp/xxw/envs/env_name/bin/pkg_name
    # 修改注释第一行