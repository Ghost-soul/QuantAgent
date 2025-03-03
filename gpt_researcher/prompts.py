import warnings
from datetime import date, datetime, timezone

from .utils.enum import ReportSource, ReportType, Tone
from typing import List, Dict, Any


def generate_search_queries_prompt(
    question: str,
    parent_query: str,
    report_type: str,
    max_iterations: int = 3,
    context: List[Dict[str, Any]] = [],
):
    """Generates the search queries prompt for the given question.
    Args:
        question (str): The question to generate the search queries prompt for
        parent_query (str): The main question (only relevant for detailed reports)
        report_type (str): The report type
        max_iterations (int): The maximum number of search queries to generate
        context (str): Context for better understanding of the task with realtime web information

    Returns: str: The search queries prompt for the given question
    """

    if (
        report_type == ReportType.DetailedReport.value
        or report_type == ReportType.SubtopicReport.value
    ):
        task = f"{parent_query} - {question}"
    else:
        task = question

    context_prompt = f"""
你是一名经验丰富的金融分析助理，负责为以下任务生成搜索查询以查找相关信息：“{task}”。
上下文：{context}

利用此上下文来指导和优化你的搜索查询。上下文提供了实时网络信息，可以帮助你生成更具体和相关的查询。请考虑上下文中提到的任何当前事件、最新情况或具体细节，以增强搜索查询的相关性。
""" if context else ""

    dynamic_example = ", ".join([f'"query {i+1}"' for i in range(max_iterations)])

    return f"""根据当前日期（假设为 {datetime.now(timezone.utc).strftime('%B %d, %Y')}）和任务“{task}”，编写 {max_iterations} 个 Google 搜索查询，以形成客观意见。

{context_prompt}
你必须以以下格式回复一个字符串列表：[{dynamic_example}]。
响应应仅包含列表。
"""


def generate_report_prompt(
    question: str,
    context,
    report_source: str,
    report_format="apa",
    total_words=1000,
    tone=None,
    language="中文",
):
    """Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            research_summary (str): The research summary to generate the report prompt for
    Returns: str: The report prompt for the given question and research summary
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
你必须在报告末尾列出所有使用的来源网址作为参考文献，并确保不重复添加来源，每个来源仅引用一次。
每个网址应以超链接形式呈现：: [url website](url)
此外，在报告中引用相关内容时，必须包含超链接指向相关网址。

例如：
作者, A. A. (年份, 月 日). 网页标题. 网站名称.[url website](url)
"""
    else:
        reference_prompt = f"""
你必须在报告末尾列出所有使用的来源文档名称作为参考文献，并确保不重复添加来源，每个来源仅引用一次。"
"""

    tone_prompt = f"以{tone.value} 的语气写金融分析报告." if tone else ""

    return f"""
信息：“{context}”
使用上述信息，回答以下查询或任务：“{question}”，并撰写一份详细的金融分析报告——
报告应聚焦于查询的答案，结构清晰、信息丰富、深入且全面，尽可能包含事实和数据，字数至少为 {total_words} 字。
你应尽量利用提供的所有相关和必要信息，撰写尽可能长的金融分析报告。

请务必遵循以下所有金融分析报告撰写指南：

你必须根据给定信息形成自己具体且有效的观点，避免使用笼统且无意义的结论。

报告必须使用 Markdown 语法，并符合 {report_format} 格式。

必须优先选择相关、可靠且重要的来源，优先选择可信来源而非不可靠来源。

如果来源可信，优先选择较新的文章而非旧文章。

使用 {report_format} 格式的文中引用参考，并在引用句子或段落的末尾以 Markdown 超链接形式标注，例如：(文中引用)。

别忘了在金融分析报告末尾添加参考文献列表，使用 {report_format} 格式，并列出完整的 URL 链接（不带超链接）。

{reference_prompt}

{tone_prompt}

金融分析报告必须使用以下语言撰写：中文。
请尽力完成，这对我的职业生涯非常重要。
假设当前日期为 {date.today()}。
"""

def curate_sources(query, sources, max_results=10):
    return f"""你的目标是评估和筛选提供的抓取内容，以完成金融分析任务：“{query}”，同时优先包含相关且高质量的信息，尤其是包含统计数据、数字或具体数据的来源。

最终的筛选列表将用作创建金融分析报告的上下文，因此请优先考虑以下内容：

尽可能保留原始信息，特别强调包含定量数据或独特见解的来源

包含广泛的观点和见解

仅过滤掉明显无关或不可用的内容

评估指南：

根据以下标准评估每个来源：

相关性：包括与查询直接或部分相关的来源。倾向于包含而非排除。

可信度：优先选择权威来源，但除非明显不可信，否则保留其他来源。

时效性：优先选择近期信息，除非旧数据至关重要或有价值。

客观性：保留带有偏见的来源，前提是它们提供了独特或补充性的观点。

定量价值：优先选择包含统计数据、数字或其他具体数据的来源。

来源选择：

尽可能包含最多相关来源，最多 {max_results} 个，注重广泛覆盖和多样性。

优先选择包含统计数据、数字数据或可验证事实的来源。

如果内容重叠但增加了深度（尤其是涉及数据时），可以接受。

仅当来源完全无关、严重过时或内容质量极差时，才将其排除。

内容保留：

不要重写、总结或压缩任何来源内容。

保留所有可用信息，仅清理明显的垃圾或格式问题。

如果来源包含有价值的数据或见解，即使相关性较低或不完整，也应保留。

待评估的来源列表：
{sources}

你必须以与原始来源完全相同的 JSON 列表格式返回响应。
响应中不得包含任何 Markdown 格式或额外文本（如 ```json），只需返回 JSON 列表！
"""




def generate_resource_report_prompt(
    question, context, report_source: str, report_format="apa", tone=None, total_words=1000, language=None
):
    """Generates the resource report prompt for the given question and research summary.

    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.

    Returns:
        str: The resource report prompt for the given question and research summary.
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
            你必须包含所有相关的来源网址。
          每个网址应以超链接形式呈现：[url website](url)
            """
    else:
        reference_prompt = f"""
            你必须在报告末尾列出所有使用的来源文档名称作为参考文献，并确保不重复添加来源，每个来源仅引用一次。
        """

    return (
        f'"""{context}"""\n\n根据上述信息，针对以下问题或主题生成一份金融分析相关文献推荐报告："{question}"。'
        f'问题或话题: "{question}". 报告应详细分析每个推荐的来源，重点关注每个来源的相关性、可靠性和重要性。'
        "确保报告结构清晰、信息丰富、深入，并遵循 Markdown 语法。\n"
        "尽可能包含相关事实、数据和数字。\n"
        f"这篇分析报告至少需要{total_words} 字.\n"
        "你必须包含所有相关的来源网址。"
        "每个网址应以超链接形式呈现：[url website](url)"
        f"{reference_prompt}"
    )


def generate_custom_report_prompt(
    query_prompt, context, report_source: str, report_format="apa", tone=None, total_words=1000, language: str = "中文"
):
    return f'"{context}"\n\n{query_prompt}'


def generate_outline_report_prompt(
    question, context, report_source: str, report_format="apa", tone=None,  total_words=1000, language: str = "中文"
):
    """Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            research_summary (str): The research summary to generate the outline report prompt for
    Returns: str: The outline report prompt for the given question and research summary
    """

    return (
        f'"""{context}""" 根据上述信息，为以下问题或主题生成一份金融分析报告的 Markdown 语法大纲："{question}"。'
        "大纲应为分析报告提供一个结构清晰的框架，包括主要部分、子部分和需要涵盖的关键点。"
        f"分析报告应详细、信息丰富、深入，且字数至少为 {total_words} 字。"
        "使用适当的 Markdown 语法格式化大纲，并确保可读性。"
    )


def generate_deep_research_prompt(
    question: str,
    context: str,
    report_source: str,
    report_format="apa",
    tone=None,
    total_words=2000,
    language: str = "中文"
):
    """Generates the deep research report prompt, specialized for handling hierarchical research results.
    Args:
        question (str): The research question
        context (str): The research context containing learnings with citations
        report_source (str): Source of the research (web, etc.)
        report_format (str): Report formatting style
        tone: The tone to use in writing
        total_words (int): Minimum word count
        language (str): Output language
    Returns:
        str: The deep research report prompt
    """
    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
你必须在报告末尾列出所有使用的来源网址作为参考文献，并确保不重复添加来源，每个来源仅引用一次。
每个网址应以超链接形式呈现：: [url website](url)
此外，在报告中引用相关内容时，必须包含超链接指向相关网址。

例如: 作者, A. A. (年份, 月 日). 网页标题. 网站名称. [url website](url)
"""
    else:
        reference_prompt = f"""
你必须在报告末尾列出所有使用的来源文档名称作为参考文献，并确保不重复添加来源，每个来源仅引用一次。"
"""

    tone_prompt = f"以 {tone.value} 的语气写这篇报告." if tone else ""
    
    return f"""
使用以下经过分层分析的信息和引用：

"{context}"

撰写一份全面的研究报告以回答该问题： "{question}"

分析报告应该满足下述要求:
1. 综合多层次分析深度的信息。
2. 整合不同分析分支的结果。
3. 呈现一个从基础到高级见解的连贯叙述。
4. 始终保持对来源的正确引用。
5. 结构清晰，包含明确的章节和子章节。
6. 字数至少为 {total_words} 字。
7. 遵循 {report_format} 格式并使用 Markdown 语法。

额外要求:
- 优先考虑从更深层次分析中得出的见解。
- 突出不同分析分支之间的联系。
- 包含相关统计数据、数据和具体示例。
- 你必须根据给定信息形成自己具体且有效的观点，避免使用笼统且无意义的结论。
- 必须优先选择相关、可靠且重要的来源，优先选择可信来源而非不可靠来源。
- 如果来源可信，优先选择较新的文章和数据而非旧文章和数据。
- 使用 {report_format} 格式的文中引用参考，并在引用句子或段落的末尾以 Markdown 超链接形式标注，例如：: ([in-text citation](url)).
- {tone_prompt}
- 以中文写作

{reference_prompt}

请撰写一份详尽且经过充分分析的报告，将所有收集到的信息综合成一个连贯的整体。
假设当前日期为 {datetime.now(timezone.utc).strftime('%B %d, %Y')}.
"""


def auto_agent_instructions():
    return """
此任务涉及对给定主题进行分析，无论该主题的复杂程度如何，也不管是否有明确的答案。研究由特定的服务器进行，服务器由其类型和角色定义，每台服务器需要不同的指令。
智能体
服务器的选择取决于主题领域以及可用于研究该主题的具体服务器名称。代理根据其专业领域进行分类，每种服务器类型都对应一个相应的表情符号。

示例：
任务：“我应该投资苹果股票吗？”
回复：
{
"server": "💰 金融智能体",
"agent_role_prompt": "你是一位经验丰富的金融分析师人工智能助手。你的主要目标是根据提供的数据和趋势，撰写全面、敏锐、公正且条理清晰的金融报告。"
}
任务：“转售运动鞋能盈利吗？”
回复：
{
"server": "📈 商业分析师智能体",
"agent_role_prompt": "你是一位经验丰富的人工智能商业分析师助手。你的主要目标是根据提供的商业数据、市场趋势和战略分析，生成全面、有见地、公正且系统结构合理的商业报告。"
}
任务：“特拉维夫最有趣的景点有哪些？”
回复：
{
"server": "🌍 旅行智能体",
"agent_role_prompt": "你是一位游历世界的人工智能导游助手。你的主要任务是根据给定地点，撰写引人入胜、有见地、公正且结构完善的旅行报告，包括历史、景点和文化见解等内容。"
}
"""


def generate_summary_prompt(query, data):
    """Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
    Returns: str: The summary prompt for the given question and text
    """

    return (
        f'{data}\n  使用上述文本，根据以下任务或查询  : "{query}"对其进行总结.\n 如果 '
        f"无法用该文本回答查询内容，你必须简要总结该文本。.\n "
        f"如果有任何事实信息，如数字、统计数据、引语等，都要包含在内 "
    )


################################################################################################

# DETAILED REPORT PROMPTS


def generate_subtopics_prompt() -> str:
    return """
提供的主要话题：

{task}

和分析数据:

{data}

构建一个子主题列表，这些子主题将作为针对该任务生成的分析报告文档的标题。
以下是一个可能的子主题列表：{子主题}。
子主题不应有重复。
子主题数量最多限制为 {最大子主题数量}。
最后，按照任务顺序对子主题进行排序，以在详细报告中呈现出相关且有意义的顺序。
“重要！”：
每个子主题必须仅与主要主题和提供的研究数据相关！

{format_instructions}
"""


def generate_subtopic_report_prompt(
    current_subtopic,
    existing_headers: list,
    relevant_written_contents: list,
    main_topic: str,
    context,
    report_format: str = "apa",
    max_subsections=5,
    total_words=800,
    tone: Tone = Tone.Objective,
    language: str = "中文",
) -> str:
    return f"""
Context:
"{context}"

主主题和子主题：
使用最新可用信息，构建关于主主题“{main_topic}”下的子主题“{current_subtopic}”的详细报告。
你必须将子章节的数量限制在最多 {max_subsections} 个。

内容重点：

分析报告应聚焦于回答问题，结构清晰、信息丰富、深入，并尽可能包含事实和数据。

使用 Markdown 语法并遵循 {report_format.upper()} 格式。

重要提示：内容与章节的唯一性：

这部分指令对于确保内容唯一性且不与现有分析报告重叠至关重要。

在撰写任何新子章节之前，请仔细查看下面提供的现有标题和现有书面内容。

避免涵盖现有书面内容中已经涉及的任何内容。

不要使用任何现有标题作为新的子章节标题。

不要重复现有书面内容中已经涵盖的信息或与其密切相关的变体，以避免重复。

如果你有嵌套的子章节，请确保它们是唯一的，并且未在现有书面内容中涵盖。

确保你的内容完全是新的，且与之前子主题报告中已涵盖的任何信息不重叠。

“现有子主题报告”：

现有子主题报告及其章节标题：

{existing_headers}

之前子主题报告中的现有书面内容：

{relevant_written_contents}

“结构与格式”：

由于此子报告将作为更大报告的一部分，仅包含分为适当子主题的主体部分，无需任何引言或结论部分。

你必须在报告中引用相关内容时包含 Markdown 超链接，例如：

章节标题
这是一个示例文本。(网址名称)

使用 H2 作为主子主题标题（##），使用 H3 作为子章节标题（###）。

使用较小的 Markdown 标题（例如 H2 或 H3）来构建内容结构，避免使用最大的标题（H1），因为它将用于更大报告的标题。

将你的内容组织成与现有报告互补但不重叠的独立章节。

当添加与现有书面内容相似或相同的子章节时，你应明确说明新内容与现有内容之间的差异。例如：

新标题（与现有标题相似）
虽然上一节讨论了[主题 A]，但本节将探讨[主题 B]。

“日期”：
如果需要，假设当前日期为 {datetime.now(timezone.utc).strftime('%B %d, %Y')}。

“重要提示！”：

你必须使用以下语言撰写报告：{language}。

重点必须放在主主题上！你必须排除任何与其无关的信息！

不得包含任何引言、结论、总结或参考文献部分。

你必须在必要时使用 Markdown 语法（网址名称）包含相关超链接。

如果你在必要时添加相似或相同的子章节，你必须在报告中提及现有内容与新内容之间的差异。

报告的最低字数为 {total_words} 字。

在整个分析报告中使用 {tone.value} 的语气。

不要添加结论部分
"""


def generate_draft_titles_prompt(
    current_subtopic: str,
    main_topic: str,
    context: str,
    max_subsections: int = 5
) -> str:
    return f"""
"上下文":
"{context}"

主主题和子主题：
使用最新可用信息，为主主题“{main_topic}”下的子主题“{current_subtopic}”构建详细报告的草稿章节标题。

任务：

为子主题报告创建一个草稿章节标题列表。

每个标题应简洁且与子主题相关。

标题不应过于笼统，而应足够详细以涵盖子主题的主要方面。

使用 Markdown 语法编写标题，使用 H3（###），因为 H1 和 H2 将用于更大报告的标题。

确保标题涵盖子主题的主要方面。

结构与格式：
使用 Markdown 语法以列表格式提供草稿标题，例如：

标题 1
标题 2
重要提示！：
子主题数量不得高于3个。
重点必须放在主主题上！你必须排除任何与其无关的信息！

不得包含任何引言、结论、总结或参考文献部分。

仅专注于创建标题，而非内容。
"""


def generate_report_introduction(question: str, research_summary: str = "", language: str = "中文") -> str:
    return f"""{research_summary}\n 
使用上述最新信息，准备关于主题“{question}”的详细分析报告引言。

引言应简洁、结构清晰、信息丰富，并使用 Markdown 语法。

由于此引言将作为更大报告的一部分，请勿包含报告中通常存在的其他部分。

引言前应有一个 H1 标题，标题应适合整个报告的主题。

你必须在必要时使用 Markdown 语法（网址名称）包含相关超链接。
如果需要，假设当前日期为 {datetime.now(timezone.utc).strftime('%B %d, %Y')}。

输出必须使用 {language} 语言。
"""


def generate_report_conclusion(query: str, report_content: str, language: str = "中文") -> str:
    """
    Generate a concise conclusion summarizing the main findings and implications of a research report.

    Args:
        query (str): The research task or question.
        report_content (str): The content of the research report.
        language (str): The language in which the conclusion should be written.

    Returns:
        str: A concise conclusion summarizing the report's main findings and implications.
    """
    prompt = f"""
分析任务：{query}  

分析报告：{report_content}  

你的结论应：  
1. 回顾之前分析的主要观点  
2. 强调最重要的发现  
3. 讨论任何影响或后续步骤  
4. 长度约为 2-3 段  

如果报告末尾没有“## 结论”部分标题，请将其添加到结论的顶部。  
你必须在必要时使用 Markdown 语法（[网址名称](url)）包含相关超链接。  

重要提示：整个结论必须使用 {language} 语言撰写。  

撰写结论：
    """

    return prompt


report_type_mapping = {
    ReportType.ResearchReport.value: generate_report_prompt,
    ReportType.ResourceReport.value: generate_resource_report_prompt,
    ReportType.OutlineReport.value: generate_outline_report_prompt,
    ReportType.CustomReport.value: generate_custom_report_prompt,
    ReportType.SubtopicReport.value: generate_subtopic_report_prompt,
    ReportType.DeepResearch.value: generate_deep_research_prompt,
}


def get_prompt_by_report_type(report_type):
    prompt_by_type = report_type_mapping.get(report_type)
    default_report_type = ReportType.ResearchReport.value
    if not prompt_by_type:
        warnings.warn(
            f"Invalid report type: {report_type}.\n"
            f"Please use one of the following: {', '.join([enum_value for enum_value in report_type_mapping.keys()])}\n"
            f"Using default report type: {default_report_type} prompt.",
            UserWarning,
        )
        prompt_by_type = report_type_mapping.get(default_report_type)
    return prompt_by_type

