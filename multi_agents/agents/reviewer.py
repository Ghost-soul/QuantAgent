from .utils.views import print_agent_output
from .utils.llms import call_model

TEMPLATE = """你是一名专业的金融分析报告审稿人。 \
你的目标是审阅分析报告草稿，并根据特定指南向修订者提供反馈。 \
"""


class ReviewerAgent:
    def __init__(self, websocket=None, stream_output=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}

    async def review_draft(self, draft_state: dict):
        """
        Review a draft article
        :param draft_state:
        :return:
        """
        task = draft_state.get("task")
        guidelines = "- ".join(guideline for guideline in task.get("guidelines"))
        revision_notes = draft_state.get("revision_notes")

        revise_prompt = f"""修订者已经根据你之前的审阅意见对草稿进行了修改，并提供了以下反馈：
{revision_notes}\n
请仅在关键问题处提供额外反馈，因为修订者已经根据你之前的反馈进行了修改。
如果你认为文章已经足够完善，或者只需要非关键性的修订，请尽量返回 None.
"""

        review_prompt = f"""你被要求根据特定指南审阅一份由非专业人士撰写的草稿。
如果草稿质量足够好，可以发布，请接受该草稿；否则，请发送修订意见以指导进一步修改。
如果草稿未完全符合指南标准，请提供适当的修订意见。
如果草稿完全符合指南要求，请返回 None。.
{revise_prompt if revision_notes else ""}

Guidelines: {guidelines}\nDraft: {draft_state.get("draft")}\n
"""
        prompt = [
            {"role": "system", "content": TEMPLATE},
            {"role": "user", "content": review_prompt},
        ]

        response = await call_model(prompt, model=task.get("model"))

        if task.get("verbose"):
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "review_feedback",
                    f"Review feedback is: {response}...",
                    self.websocket,
                )
            else:
                print_agent_output(
                    f"Review feedback is: {response}...", agent="REVIEWER"
                )

        if "None" in response:
            return None
        return response

    async def run(self, draft_state: dict):
        task = draft_state.get("task")
        guidelines = task.get("guidelines")
        to_follow_guidelines = task.get("follow_guidelines")
        review = None
        if to_follow_guidelines:
            print_agent_output(f"Reviewing draft...", agent="REVIEWER")

            if task.get("verbose"):
                print_agent_output(
                    f"Following guidelines {guidelines}...", agent="REVIEWER"
                )

            review = await self.review_draft(draft_state)
        else:
            print_agent_output(f"Ignoring guidelines...", agent="REVIEWER")
        return {"review": review}
