from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm import summarize
from cleaner import clean_pdf
from splitter import chunking

def pdf_ingestion(file_path):
    loader = PyPDFLoader(file_path)
    raw_docs = loader.load()
    cleaned_docs = clean_pdf(raw_docs)
    chunks = chunking(cleaned_docs)
    final_summary = summarize(chunks)
    return final_summary

if __name__ == "__main__":
    res = pdf_ingestion("attention_is_all_you_need.pdf")
    print(res)

