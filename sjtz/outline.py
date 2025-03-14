from datetime import datetime
from call_model import call_model
today = datetime.now().strftime('%d/%m/%Y')
def get_outline(prompt):
    content = f"""今天是{today}
                   研究摘要报告: '{prompt}'
                   \n你的任务是根据上述分析摘要报告生成各章节的标题大纲,这里必须紧扣'{prompt}'。
                   你只需返回一个 JSON，结构如下
                   '{{title: string research title, date: today's date, 
                   sections: ['section header 1', 'section header 2', 'section header 3']}}'
                   其中section header 1 只进行对应的行业分析及宏观背景分析,包括宏观经济环境，政府政策，技术创新等方面。
                   section header 2 只进行近期A股市场投资者的情绪分析,尤其针对该行业结合股票市场近一周情况进行分析。
                   section header 3 只通过技术分析方法分析股票交易数据并给出未来可能的走势。
                   """
    outline = call_model(content)
    return outline

