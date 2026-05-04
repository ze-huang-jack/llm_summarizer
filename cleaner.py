import re


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


