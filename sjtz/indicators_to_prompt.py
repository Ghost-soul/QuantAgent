from technical_analysis import technical_analysis
from call_model import call_model
def indicators_to_prompt(codes):
    prompts = ""
    for code in codes:
        result = technical_analysis(code)
        prompt = f"""股票代码：{code}
        技术指标: {result}
        """
        prompts += prompt
    content = call_model("下面是个股的技术分析："+prompts+"你的任务是将上述技术分析结果，按照股票代码进行整理，在K线形态判断上，请去除相似项，仅保留典型的K线特征。返回格式为股票代码：技术分析结果。无需返回其它内容。")
    return content