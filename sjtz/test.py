import json
from gpt_researcher import GPTResearcher
import asyncio
import os
import sys
from dotenv import load_dotenv
from outline import get_outline
import time
from datetime import datetime
from call_model import call_model
from indicators_to_prompt import indicators_to_prompt
dir = os.path.dirname(__file__)
load_dotenv(r"C:\Users\zyx\Desktop\s\QuantAgent\sjtz\.env")
today = datetime.now().strftime('%Y/%m/%d')
#print(os.getenv("NOMIC_API_KEY"))
async def get_research_report(query: str, report_type: str, report_source: str,config_path:str) -> str:
    researcher = GPTResearcher(query=query, report_type=report_type, report_source=report_source,config_path=config_path)
    research = await researcher.conduct_research()
    report = await researcher.write_report()
    return report
async def industry(prompt: str) -> str:
    result = await get_research_report(query=f"今天是{today},你是一位专业的行业研究员与宏观分析师,你的目标是撰写一篇优秀，简短，高质量的金融分析报告。行业研究需“由外到内”（宏观→行业→企业）、“由静到动”（现状→趋势），结合定量数据（市场规模、财务指标）与定性洞察（政策、技术变革），综合运用不同的分析方法（趋势分析、归因分析、价值分析等），并结合行业动态（政策、技术、行业事件等），对行业未来发展趋势进行分析，不需要进行个股分析，不少于1500字。请你结合最近一年数据只进行行业分析与宏观背景分析,主题是："+prompt, report_type="research_report", report_source="Hybrid",config_path=os.path.join(dir, "industry.json"))
    return result

async def sentiment(prompt: str) -> str:
    result = await get_research_report(query=f"今天是{today}，你是一位专业的金融市场情绪分析专家。你的任务是从网络上和本地数据库中捕捉能反映当前A股市场情绪的消息和新闻或者指数，分析金融市场给定行业的投资者情绪，并提供详细的分析结果，不少于1000字。你的回答应该包括以下内容：1. 对A股市场整体投资者情绪进行分析。2. 对该行业的投资者情绪进行分析；3. 对造成该行业投资者情绪变化的主要原因进行分析；4. 对该行业投资情绪对A股市场的的主要影响进行分析；请你结合最近一周数据只进行投资者情绪分析,主题是："+prompt,report_type="custom_report", report_source="Hybrid",config_path=os.path.join(dir, "sentiment.json"))
    return result

async def technique(tec: str) -> str:
    result = await get_research_report(query=f"你是一位专业的金融市场技术分析专家，你的任务是根据给定的数据，使用专业的金融市场技术分析方法和工具，对个股进行深入的分析和研究，其中在K线形态上可以结合动量指标和布林轨道展开分析，不少于1000字。在这里只对个股进行技术分析，数据如下："+tec, report_type="custom_report", report_source="local",config_path=os.path.join(dir,"technique.json"))
    return result

async def memory(prompt: str) -> str:
    result = await get_research_report(query=f"""请你依据{prompt},检索本地历史报告,结合报告反馈给出具体的投资建议，并给出相应的买入与卖出策略，格式为 1.xx股票 对应技术和指标，对应的的分析结果与交易策略；2.xx股票 对应技术和指标，对应的的分析结果与交易策略；3.xx股票 对应技术和指标，对应的分析结果与交易策略...并按推荐度从高到低进行排序。不少于1000字""", report_type="custom_report", report_source="Local",config_path=os.path.join(dir,"memory.json"))
    return result
async def results(prompt,tec):
    result = await asyncio.gather(industry(prompt), sentiment(prompt), technique(tec))
    return result

def outputs(prompt,codes,path):
    industry_report, sentiment_report, technique_report = asyncio.run(results(prompt,codes))
    draft = f"""
          Title: 金融分析报告,
          Date: {today}, 
          section1:行业研究及宏观背景分析
          section2:市场情绪分析
          section3:技术面分析
          summary:结论与投资建议
          参考文献                   """
    
    tem_draft = draft
    prompt1 = f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{industry_report}'
    草稿: '{tem_draft}'
    任务：你现在正在攥写草稿中section1:行业研究及宏观背景分析部分，该部分只进行对应的行业分析及宏观背景分析,包括宏观经济环境，政府政策，技术创新等方面。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在文中注明。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    请仅返回撰写后的section1:行业研究及宏观背景分析部分。
    """
    section1 = call_model(content = prompt1)

    tem_draft = draft.replace("section1:行业研究及宏观背景分析",section1)
    prompt2 = f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{sentiment_report}'
    草稿: '{tem_draft}'
    任务：你现在正在攥写草稿中section2:市场情绪分析部分，该部分只进行近期A股市场投资者情绪分析。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在文中注明。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    请仅返回撰写后的section2:市场情绪分析部分。
    """
    section2 = call_model(content = prompt2)

    tem_draft = draft.replace("section2:市场情绪分析",section2)
    prompt3 =f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{technique_report}'
    草稿: '{tem_draft}'
    任务：你现在正在攥写草稿中section3:技术面分析部分，该部分只通过使用技术分析方法分析股票交易数据并给出未来可能的走势。你应该尽可能保留文章分析结果，不要自己编造数据，在这节无需给出对应的交易策略。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在文中注明。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    请仅返回撰写后的section3:技术面分析部分。
    """
    section3 = call_model(content = prompt3)

    tem_draft = draft.replace("section1:行业研究及宏观背景分析",section1).replace("section2:市场情绪分析",section2).replace("section3:技术面分析",section3)
    
    memory_report = asyncio.run(memory(tem_draft))
    
    prompt4 =f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{memory_report}'
    草稿: '{tem_draft}'
    任务：你现在正在攥写草稿中summary:结论与投资建议部分，该部分需要给出具体的投资建议，并给出相应的买入与卖出策略，格式为 1.xx股票 对应的分析结果；2.xx股票 对应的分析结果；3.xx股票 对应的分析结果...并按推荐度从高到低进行排序,不超过5只股票。你应该尽可能保留文章分析结果，不要自己编造数据。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在文中注明。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    请仅返回撰写后的summary:结论与投资建议部分。
    """
    summary = call_model(content = prompt4)

    result = draft.replace("section1:行业研究及宏观背景分析",section1).replace("section2:市场情绪分析",section2).replace("section3:技术面分析",section3).replace("summary:结论与投资建议",summary)
    with open(os.path.join(path,"try\\writer_report.md"), "w", encoding="utf-8") as file:
            file.write(result)

    prom = f"""你是一位专业的金融分析报告编辑,你的目标是根据markdown语法对报告在初稿基础上进行细微修改。
    报告: '{result}'
    要点：务必保证原报告结构的完整性，字数不得低于原报告。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
    只需返回修改后的金融分析报告全文。
    """
    revise_report = call_model(content= prom)

    with open(os.path.join(path,"try\\revise_report.md"), "w", encoding="utf-8") as file:
        file.write(revise_report)
    return revise_report


if __name__ == "__main__":
    t1 = time.time()
    print(os.getenv("NOMIC_API_KEY"))
    print(os.getenv("TAVILY_API_KEY"))
    prompt = "请帮我分析一下A股市场有色金属 铜相关板块各股并给出投资建议"
    codes = indicators_to_prompt(["601899","603993","600362","601168","000630","603979","000878","601212","002203","000737","002171","601609","600490"])
    outputs(prompt = prompt,codes = codes,path = dir)
    t2 = time.time()
    print(t2-t1)



    