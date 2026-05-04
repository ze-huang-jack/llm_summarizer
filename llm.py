import os

from dotenv import load_dotenv
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

raw_client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
client = wrap_openai(raw_client)

@traceable(
    run_type="llm",
    name="deepseek chat",
    metadata={"ls_provider": "DeepSeek", "ls_model_name": "DeepSeek/deepseek-v4-flash"},
)
def summarize(chunks):
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        openai_api_key=os.getenv("API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )

    # Map 阶段：对每个 chunk 提炼要点
    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "请提炼以下文本的核心要点，输出简洁的要点列表。"),
        ("user", "{chunk}")
    ])
    map_chain = map_prompt | llm | StrOutputParser()

    # Reduce 阶段：合并所有要点并生成结构化 Markdown 报告
    reduce_prompt = ChatPromptTemplate.from_messages([
        ("system", "请根据以下所有要点，生成一份结构化 Markdown 报告，包含以下三部分：\n\n## 核心主题\n\n## 关键点提取\n\n## 金句总结\n\n请确保输出格式为 Markdown。"),
        ("user", "{combined}")
    ])
    reduce_chain = reduce_prompt | llm | StrOutputParser()

    # Map 阶段：并行处理 chunks，容错处理
    map_results = []
    for idx, chunk in enumerate(chunks):
        try:
            result = map_chain.invoke({"chunk": chunk})
            map_results.append(result)
        except Exception as e:
            # 记录失败，但不中断整体流程
            print(f"[Map 阶段] 第 {idx+1} 个 chunk 处理失败：{e}")
            continue

    if not map_results:
        return "### 错误：所有分片处理失败，无法生成总结。"

    combined = "\n\n".join(map_results)

    # Reduce 阶段：生成最终报告
    try:
        final_report = reduce_chain.invoke({"combined": combined})
        return final_report
    except Exception as e:
        return f"### 错误：Reduce 阶段失败，无法生成最终报告。\n\n中间要点如下：\n\n{combined}"
