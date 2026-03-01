"""API 测试脚本"""

import base64

import requests
from openai import OpenAI

base_url = "http://localhost:8000/v1/"

# 配置 API Key（需要在 .env 中配置）
api_key = "sk-test-api-key"

chat_id = ""  # 可选，如果不提供会自动创建

# 上传文件（可选）
upload_url = base_url + "upload"

try:
    file_name = "qrcode.png"
    with open(file_name, "rb") as f:
        file_data = base64.b64encode(f.read()).decode("utf-8")
    data = {
        "file": {
            "file_name": file_name,
            "file_data": file_data,
            "file_type": "image",  # image、doc、excel、pdf等
        },
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(upload_url, json=data, headers=headers)
    if response.status_code == 200:
        print("File uploaded successfully:", response.json())
        multimedia = [response.json()]
    else:
        print("File upload failed:", response.status_code, response.text)
        multimedia = []
except FileNotFoundError:
    print(f"File {file_name} not found, skipping upload")
    multimedia = []

print(f"Multimedia: {multimedia}")

# 聊天请求
client = OpenAI(base_url=base_url, api_key=api_key)

response = client.chat.completions.create(
    model="deepseek-v3",
    messages=[{"role": "user", "content": "这是什么？"}],
    stream=True,
    extra_body={
        "chat_id": chat_id,
        "should_remove_conversation": False,
        "multimedia": multimedia,
    },
)

print("\nResponse:")
for chunk in response:
    print(chunk.choices[0].delta.content or "")
print("\n")
