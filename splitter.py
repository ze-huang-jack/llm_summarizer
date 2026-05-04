from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunking(cleaned_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(cleaned_text)
    return chunks
