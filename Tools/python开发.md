## Jupyter Notebook
* Reload Modules:
    - re-execute import不生效问题：首次import modules后，the changes may not be reflected because Python's import system caches the imported modules，除非restart kernel。使用iPython的[autoreload magic方法](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html)可以解决这个问题：
        ```python
        # 在首次import前添加执行magic模块
        # 下为示例
        %load_ext autoreload
        %autoreload 2
        from configs import DB_BGEM3