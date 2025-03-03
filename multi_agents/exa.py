"""from gpt_researcher import GPTResearcher
import asyncio
import os
from dotenv import load_dotenv
if os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
load_dotenv()
async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    await researcher.conduct_research()
    report = await researcher.write_report()
    return report

if __name__ == "__main__":
    query = "为什么A股涨少跌多?"
    report_type = "research_report"
    report = asyncio.run(get_report(query, report_type))
    print(report)
"""
import os
from openai import OpenAI

client = OpenAI(
    # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-zVz0CAJ9YcbfdDX45rR2nAh7259Sfl9betsMNn51zg5cxk1y", # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
    base_url="https://api.lkeap.cloud.tencent.com/v1",
)

completion = client.chat.completions.create(
    model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '9.9和9.11谁大'}
        ]
)

# 通过reasoning_content字段打印思考过程
print("思考过程：")
print(completion.choices[0].message.reasoning_content)
# 通过content字段打印最终答案
print("最终答案：")
print(completion.choices[0].message.content)