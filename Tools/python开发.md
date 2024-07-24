## Jupyter Notebook
* Reload Modules:
    - re-execute import不生效问题：首次import modules后，the changes may not be reflected because Python's import system caches the imported modules，除非restart kernel。使用iPython的[autoreload magic方法](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html)可以解决这个问题：
        ```python
        # 在首次import前添加执行magic模块
        # 下为示例
        %load_ext autoreload
        %autoreload 2
        from configs import DB_BGEM3


## Pydantic
Pydantic是一个主要应用于数据parsing & validation 的包，BaseModel是其中一个primary class, You can create data models by ***subclassing BaseModel*** and defining attributes with type annotations:
    ```python
    from pydantic import BaseModel, ValidationError
    from typing import List, Optional

    class User(BaseModel):
        id: int
        name: str
        signup_ts: Optional[str] = None
        friends: List[int] = []

    # Valid data example
    user_data = {
        'id': 1,
        'name': 'John Doe',
        'signup_ts': '2023-07-21T12:34:56',
        'friends': [2, 3, 4]
    }

    user = User(**user_data)
    print(user)
    print(user.id)
    print(user.name)

    # Invalid data example
    invalid_user_data = {
        'id': 'abc',  # id should be an int
        'name': 'Jane Doe',
        'signup_ts': '2023-07-21T12:34:56',
        'friends': [2, 3, 4]
    }

    try:
        invalid_user = User(**invalid_user_data)
    except ValidationError as e:
        print(e)
* Key Points:
    - Automatic Validation: 报错时会输出详细信息
    - Data Parsing: Pydantic can parse and convert data types. For example, it can ***parse strings*** into datetime objects, integers, and other types as needed.