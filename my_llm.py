import requests
import json
import os

def getEnvJson():
    # 获取当前脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件的绝对路径
    env_path = os.path.join(script_dir, 'env.json')
    with open(env_path, 'r') as f:
        return json.load(f)

env_data = getEnvJson()
url = env_data["API_URL"]
model = env_data["MODEL"]
api_key = env_data["API_KEY"]

payload = {
    "model": model,
    "stream": False,
    "max_tokens": 512,
    "thinking_budget": 4096,
    "min_p": 0.05,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "stop": [],
    "messages": [
        {
            "role": "user",
            "content": "test"
        }
    ]
}
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 调用LLM服务的核心函数
# 参数:
#   messages: 消息列表，包含对话历史，格式为[{"role": "user", "content": "问题"}, ...]
#   enable_thinking: 是否启用思考模式
# 返回值:
#   requests.Response对象，包含LLM的响应
# 异常:
#   如果API调用失败(状态码不是200)，则抛出异常
def llm(messages, enable_thinking):
    # 更新请求的消息部分
    payload["messages"] = messages
    # 如果启用思考模式，添加相应参数
    if enable_thinking:
        payload["enable_thinking"] = True
    # 发送POST请求到LLM API
    response = requests.request("POST", url, json=payload, headers=headers)
    # 检查响应状态，非200则抛出异常
    if response.status_code != 200:
        raise Exception(response.text)
    return response

# 从LLM响应中提取推理内容
# 参数:
#   response: requests.Response对象，LLM的响应
# 返回值:
#   字符串，推理内容，如果不存在则返回空字符串
def get_reasoning_content(response):
    # 解析响应JSON数据
    json_data = json.loads(response.text)
    # 提取推理内容，不存在则返回空字符串
    if json_data["choices"][0]["message"]["reasoning_content"]:
        return json_data["choices"][0]["message"]["reasoning_content"]
    else:
        return ""

# 从LLM响应中提取主要内容
# 参数:
#   response: requests.Response对象，LLM的响应
# 返回值:
#   字符串，LLM的主要回答内容
def get_content(response):
    # 解析响应JSON数据
    json_data = json.loads(response.text)
    # 提取主要内容
    return json_data["choices"][0]["message"]["content"]

# 测试函数，简单测试api
def test_api():
    try:
        # 构造测试消息
        test_messages = [{"role": "user", "content": "请回答“Hello”"}]
        # 调用 llm 函数，启用思考模式
        resp = llm(test_messages, enable_thinking=True)
        # 打印推理内容
        print("推理内容：", get_reasoning_content(resp))
        print("*****************************")
        # 打印主要内容
        print("主要内容：", get_content(resp))
    except Exception as e:
        print("测试失败：", e)

if __name__ == "__main__":
    test_api()
