import os
from openai import OpenAI
def call_model(content):
    client = OpenAI(
        # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-zVz0CAJ9YcbfdDX45rR2nAh7259Sfl9betsMNn51zg5cxk1y", # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
        base_url="https://api.lkeap.cloud.tencent.com/v1",
    )
    completion = client.chat.completions.create(
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': "user", 'content': content}
            ]
    )
    return completion.choices[0].message.content
