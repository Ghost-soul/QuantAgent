from .utils.views import print_agent_output
from .utils.llms import call_model
import json

sample_revision_notes = """
{
  "draft": { 
    draft title: 你提交供审阅的修订草案 
  },
  "revision_notes": 你向审阅者传达的关于根据其反馈对草案所做修改的内容与信息
}
"""


class ReviserAgent:
    def __init__(self, websocket=None, stream_output=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}

    async def revise_draft(self, draft_state: dict):
        """
        Review a draft article
        :param draft_state:
        :return:
        """
        review = draft_state.get("review")
        task = draft_state.get("task")
        draft_report = draft_state.get("draft")
        prompt = [
            {
                "role": "system",
                "content": "你是一位专业的金融分析报告写作者,你的目标是根据审阅者的意见对草案进行修订。"
            },
            {
                "role": "user",
                "content": f"""Draft:\n{draft_report}" + "Reviewer's notes:\n{review}\n\n
你被审阅者委以重任，负责修订一份由非专业人士撰写的草案。
如果你决定遵循审阅者的意见，请撰写一份新草案，并确保解决他们提出的所有问题。
请保持草案的其他所有方面不变。
你必须仅返回以下格式的 JSON：
{sample_revision_notes}
""",
            },
        ]

        response = await call_model(
            prompt,
            model=task.get("model"),
            response_format="json",
        )
        return response

    async def run(self, draft_state: dict):
        print_agent_output(f"Rewriting draft based on feedback...", agent="REVISOR")
        revision = await self.revise_draft(draft_state)

        if draft_state.get("task").get("verbose"):
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "revision_notes",
                    f"Revision notes: {revision.get('revision_notes')}",
                    self.websocket,
                )
            else:
                print_agent_output(
                    f"Revision notes: {revision.get('revision_notes')}", agent="REVISOR"
                )

        return {
            "draft": revision.get("draft"),
            "revision_notes": revision.get("revision_notes"),
        }
