## Fastchat
- call funcs of controller and worker(ref to git code): 
    ```python
    # json请求数据optional
    ret = requests.post(url+'/'+func_name, json={})


## OpenAI Chat API
- Curl 请求对话命令：
    ```sh
    curl http://localhost:8000/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
            "model": "glm-4-9b-chat-1m",
            "messages": [{"role": "user", "content": "你好}]
        }'