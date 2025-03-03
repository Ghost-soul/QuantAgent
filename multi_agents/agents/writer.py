from datetime import datetime
import json5 as json
from .utils.views import print_agent_output
from .utils.llms import call_model

sample_json = """
{
  "table_of_contents": 基于金融分析报告标题和子标题的目录（使用 Markdown 语法，以 '-' 表示）,
  "introduction": 关于该主题的深入分析（使用 Markdown 语法，并包含相关来源的超链接引用）,
  "conclusion": 基于所有分析数据的总结（使用 Markdown 语法，并包含相关来源的超链接引用）,
  "sources": 分析中使用的所有来源链接列表（使用 Markdown 语法和 APA 引用格式）。例如：['- 标题, 年份, 作者 [来源链接](链接)', ...]，
}
"""


class WriterAgent:
    def __init__(self, websocket=None, stream_output=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers

    def get_headers(self, research_state: dict):
        return {
            "title": research_state.get("title"),
            "date": "Date",
            "introduction": "Introduction",
            "table_of_contents": "Table of Contents",
            "conclusion": "Conclusion",
            "references": "References",
        }

    async def write_sections(self, research_state: dict):
        query = research_state.get("title")
        data = research_state.get("research_data")
        task = research_state.get("task")
        follow_guidelines = task.get("follow_guidelines")
        guidelines = task.get("guidelines")

        prompt = [
            {
                "role": "system",
                "content": "你是一位金融分析报告写作者。你的唯一目标是根据金融分析结果和信息，撰写一篇关于某个主题的优秀分析报告。",
            },
            {
                "role": "user",
                "content": f"今天是{datetime.now().strftime('%d/%m/%Y')}\n."
                f"Query or Topic: {query}\n"
                f"Research data: {str(data)}\n"
                f"你的任务是根据提供的分析数据为分析报告撰写深入、优秀且详细的引言和结论。不要在结果中包含标题。\n"
                f"结论部分应根据上文分析的结果给出具体的投资建议，格式为 1.xx股票 对应的分析结果；2.xx股票 对应的分析结果；3.xx股票 对应的分析结果..."
                f"你必须将任何相关来源作为 markdown 超链接包含在引言和结论中-"
                f"例如: '这是一个示例文本. ([url website](url))'\n\n"
                f"{f'你必须遵循提供的指导方针: {guidelines}' if follow_guidelines else ''}\n"
                f"您只能返回以下格式的 JSON（不带 json markdown）：\n"
                f"{sample_json}\n\n",
            },
        ]

        response = await call_model(
            prompt,
            task.get("model"),
            response_format="json",
        )
        return response

    async def revise_headers(self, task: dict, headers: dict):
        prompt = [
            {
                "role": "system",
                "content": """你是一名金融分析报告写作者，你唯一的任务是根据给定的guidelines修改标题数据。""",
            },
            {
                "role": "user",
                "content": f"""你的任务是根据给定的guidelines修订所提供的 headers JSON。
你需要遵循guidelines，但值应为简单的字符串，忽略所有 Markdown 语法。
你必须仅返回与标题数据相同格式的 JSON。
Guidelines: {task.get("guidelines")}\n
Headers Data: {headers}\n
""",
            },
        ]

        response = await call_model(
            prompt,
            task.get("model"),
            response_format="json",
        )
        return {"headers": response}

    async def run(self, research_state: dict):
        if self.websocket and self.stream_output:
            await self.stream_output(
                "logs",
                "writing_report",
                f"Writing final research report based on research data...",
                self.websocket,
            )
        else:
            print_agent_output(
                f"Writing final research report based on research data...",
                agent="WRITER",
            )

        research_layout_content = await self.write_sections(research_state)

        if research_state.get("task").get("verbose"):
            if self.websocket and self.stream_output:
                research_layout_content_str = json.dumps(
                    research_layout_content, indent=2
                )
                await self.stream_output(
                    "logs",
                    "research_layout_content",
                    research_layout_content_str,
                    self.websocket,
                )
            else:
                print_agent_output(research_layout_content, agent="WRITER")

        headers = self.get_headers(research_state)
        if research_state.get("task").get("follow_guidelines"):
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "rewriting_layout",
                    "Rewriting layout based on guidelines...",
                    self.websocket,
                )
            else:
                print_agent_output(
                    "Rewriting layout based on guidelines...", agent="WRITER"
                )
            headers = await self.revise_headers(
                task=research_state.get("task"), headers=headers
            )
            headers = headers.get("headers")

        return {**research_layout_content, "headers": headers}
