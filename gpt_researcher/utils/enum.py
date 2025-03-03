from enum import Enum


class ReportType(Enum):
    ResearchReport = "research_report"
    ResourceReport = "resource_report"
    OutlineReport = "outline_report"
    CustomReport = "custom_report"
    DetailedReport = "detailed_report"
    SubtopicReport = "subtopic_report"
    DeepResearch = "deep"


class ReportSource(Enum):
    Web = "web"
    Local = "local"
    Azure = "azure"
    LangChainDocuments = "langchain_documents"
    LangChainVectorStore = "langchain_vectorstore"
    Static = "static"
    Hybrid = "hybrid"


class Tone(Enum):
    Objective = "客观（公正且无偏见地呈现事实和发现）"

    Formal = "正式（遵循学术标准，使用复杂的语言和结构）"

    Analytical = "分析性（对数据和理论进行批判性评估和详细检查）"

    Persuasive = "说服性（说服观众接受特定观点或论点）"

    Informative = "信息性（提供关于主题的清晰且全面的信息）"

    Explanatory = "解释性（澄清复杂的概念和过程）"

    Descriptive = "描述性（详细描述现象、实验或案例研究）"

    Critical = "批判性（判断研究及其结论的有效性和相关性）"

    Comparative = "比较性（并列不同的理论、数据或方法，以突出差异和相似之处）"

    Speculative = "推测性（探索假设及其潜在影响或未来研究方向）"

    Reflective = "反思性（考虑研究过程及个人见解或经验）"

    Narrative = "叙述性（通过讲故事来说明研究发现或方法论）"

    Humorous = "幽默性（轻松愉快且引人入胜，通常使内容更易于理解）"

    Optimistic = "乐观性（强调积极发现和潜在益处）"

    Pessimistic = "悲观性（关注局限性、挑战或负面结果）"
