import re

from langchain_core.documents import Document


def clean_srt(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    #  移除时间轴
    # 匹配类似 00:00:05,520 --> 00:00:08,080
    text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', raw_text)

    #  移除序号 (单独成行的数字)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)

    #  移除常见字幕标签 (如 <i>...</i>)
    text = re.sub(r'<[^>]+>', '', text)


    text = re.sub(r'\[[^]]+]', '', text)

    #  清理多余空格和换行
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    #  合并成连续文本
    cleaned_text = " ".join(lines)
    return cleaned_text


def clean_pdf(raw_docs):
    """
    清洗 PDF 文本：去噪、结构修复、内容过滤，返回纯文本字符串。
    """
    if not raw_docs:
        return ""

    pure_text_list = []

    # 预编译正则，提升长文本处理性能
    re_hyphen_nl = re.compile(r'(\w)-\n(\w)')
    re_inner_nl = re.compile(r'(?<=[^\n])\n(?=[^\n])')
    re_tag = re.compile(r'<[^>]+>')
    re_bracket = re.compile(r'\[[^]]+]', re.MULTILINE)
    re_page_num = re.compile(r'^\s*\d+\s*$', re.MULTILINE)
    re_date = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b')
    re_filename = re.compile(r'\b\w+\.pdf\b', re.IGNORECASE)
    re_garbage = re.compile(r'[^ \w\n.,;:!?\'"()\-–—]', re.UNICODE)

    for doc in raw_docs:
        content = doc.page_content
        if not content:
            continue

        # 内容过滤：少于 10 字符或乱码比例过高直接丢弃
        stripped = content.strip()
        if len(stripped) < 10:
            continue
        if len(re_garbage.findall(stripped)) / len(stripped) > 0.2:
            continue

        # 结构修复：连字符断词 & 段落内换行
        content = re_hyphen_nl.sub(r'\1\2', content)
        content = re_inner_nl.sub(' ', content)

        # 去标签
        content = re_tag.sub('', content)
        content = re_bracket.sub('', content)

        # 去噪：页码、日期、文件名等冗余元数据
        content = re_page_num.sub('', content)
        content = re_date.sub('', content)
        content = re_filename.sub('', content)

        # 空间压缩：保留段落间双换行
        content = re.sub(r'[ \t]+', ' ', content)
        content = re.sub(r'[ \t]*\n[ \t]*', '\n', content)
        content = re.sub(r'\n{3,}', '\n\n', content)

        pure_text_list.append(content.strip())

    final_text = "\n\n".join(pure_text_list)
    return final_text



