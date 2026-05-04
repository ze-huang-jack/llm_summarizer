from cleaner import clean_srt
from splitter import chunking
from llm import summarize

def main():
    file_name = "subtitles.srt"
    # 调用清洗函数，对原始字幕文本进行清理
    final_text = clean_srt(file_name)
    # 调用分块函数，将清洗后的字幕文本切分成若干块
    chunks = chunking(final_text)
    # 调用摘要函数，对分块后的文本进行摘要
    summary = summarize(chunks)
    print(summary)

if __name__ == "__main__":
    main()
