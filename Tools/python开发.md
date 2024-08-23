# Python开发

## Python环境
* ***issue***: -bash: /mnt/glusterfs/rscb/nlp/xxw/envs/qwen2/bin/ninja: /mnt/glusterfs101/rscb/nlp/xxw/envs/qwen/bin/python: bad interpreter: No such file or directory<br>
    ***solution***: 
    ```cli
    vim /mnt/glusterfs/rscb/nlp/xxw/envs/env_name/bin/pkg_name
    # 修改注释第一行
* **国内镜像源**
    * 阿里：https://mirrors.aliyun.com/pypi/simple/


## Jupyter Notebook
* Reload Modules: re-execute import不生效问题：首次import modules后，the changes may not be reflected because Python's import system caches the imported modules，除非restart kernel。使用iPython的[autoreload magic方法](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html)可以解决这个问题：
        ```python
        # 在首次import前添加执行magic模块
        # 下为示例
        %load_ext autoreload
        %autoreload 2
        from configs import DB_BGEM3


## Http Request/Response
### Request
* URL
* Method: GET, POST...
* status code
* Headers: key-value pairs, provide additional information to the server.
    - Content-Type: Indicates the media type of the resource or the data being sent in the request body.
    - Authorization, User-Agent, Accept...
* Body(optional): The body could be either in the json or xml format.
### Response
* Headers
* Body

## API
### FastAPI
[FastAPI](https://fastapi.tiangolo.com/)是最流行的基于python的web API框架:
* 接口方法支持[http的定义方法](https://www.w3schools.com/tags/ref_httpmethods.asp)
* 接口方法**extract params from request body**(参数定义和验证):
    - Body(): 对单个参数的定义和验证
        ```python
        # Body(...) 表示该参数为必须参数
        param_name: data_type = Body(.../default_value, description="", example="")
    - Pydantic Model
        ```python
        from pydantic import BaseModel
        class InputData(BaseModel):
            param_name: data_type (= default_value)
* 接口方法**return data to response body**(响应返回内容):
    - [返回响应数据的五种常见方式](https://cloud.tencent.com/developer/article/1886087)
    - Pydantic Model示例
        ```python
        class ResponseModel(BaseModel):
            message: str
            data: Optional[Any] = None
            warnings: Optional[List[str]] = None
            errors: Optional[List[str]] = None


### WebSocket和RESTful API
WebSocket和RESTful API是用于在客户端和服务器之间进行通信的不同协议。
* RESTful API（Representational State Transfer）是一种使用HTTP协议进行通信的架构风格。它基于客户端-服务器模型，通过使用不同的HTTP动词（GET、POST、PUT、DELETE等）对资源进行操作。RESTful API是基于请求/响应模型的，客户端发起请求，服务器对请求进行处理并返回响应。每次请求都是无状态的，意味着服务器不会记住先前的请求状态。
* WebSocket是一种持久化的、全双工通信协议，它允许在客户端和服务器之间进行实时的双向通信。WebSocket通过一个单独的长连接（WebSocket连接）进行通信，而不是每次请求都创建新的连接。这意味着服务器可以主动地向客户端推送数据，而不需要客户端使用轮询或定时器等方式进行长时间的查询。
* 区别：
    - RESTful API是基于请求/响应模型的，每次请求都是无状态的，服务器不会主动向客户端推送数据。WebSocket则是通过单个长连接进行实时的双向通信，服务器可以主动向客户端推送数据。
    - RESTful API使用HTTP协议，常用于通过标准的HTTP动词对服务器上的资源进行增删改查操作。WebSocket则是一种独立的协议，通常运行在HTTP之上。
    - RESTful API适用于那些需要按需请求资源的场景，例如获取数据库中的数据。WebSocket适用于需要实时双向通信的场景，例如实时聊天、实时数据更新等。
    - 选择使用RESTful API还是WebSocket取决于你的应用程序需求。如果只需要按需获取资源，可以选择RESTful API。如果需要实时的双向通信，可以选择WebSocket。


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