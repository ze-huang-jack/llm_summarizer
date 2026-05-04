from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
def chunking(
    cleaned_text: str,
    chunk_size: int = 2000,
    chunk_overlap: int = 100,
    separators: Optional[List[str]] = None
) -> List[str]:
    """
    将清洗后的文本按指定规则分块。

    参数:
        cleaned_text (str): 已清洗的输入文本。
        chunk_size (int): 每块最大字符数，默认 2000。
        chunk_overlap (int): 相邻块重叠字符数，默认 100。
        separators (Optional[List[str]]): 自定义分隔符列表，优先按顺序切分。
            默认使用 RecursiveCharacterTextSplitter 内置分隔符。

    返回:
        List[str]: 分块后的字符串列表。

    异常:
        ValueError: 当 chunk_size <= 0 或 chunk_overlap < 0 或 chunk_overlap >= chunk_size 时抛出。
    """
    if not isinstance(cleaned_text, str):
        raise TypeError("cleaned_text 必须是字符串类型")
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap 不能为负数")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须小于 chunk_size")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    chunks = text_splitter.split_text(cleaned_text)
    return chunks
