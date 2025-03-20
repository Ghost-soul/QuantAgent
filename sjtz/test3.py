from gpt_researcher import GPTResearcher
import os
from dotenv import load_dotenv
import asyncio
dir = os.path.dirname(__file__)
load_dotenv(r"C:\Users\zyx\Desktop\s\QuantAgent\sjtz\.env")
print(os.getenv("TAVILY_API_KEY"))
print(os.getenv("NOMIC_API_KEY"))
async def get_research_report(query: str, report_type: str, report_source: str,config_path:str) -> str:
    researcher = GPTResearcher(query=query, report_type=report_type, report_source=report_source,config_path=config_path)
    research = await researcher.conduct_research()
    report = await researcher.write_report()
    return report
async def industry(prompt: str) -> str:
    result = await get_research_report(query=prompt, report_type="research_report", report_source="hybrid",config_path=os.path.join(dir, "industry.json"))
    return result
result = asyncio.run(industry("有色金属投资，尤其是铜 相关行业"))
print(result)