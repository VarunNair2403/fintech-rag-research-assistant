from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

CHROMA_DIR = str(ROOT_DIR / ".chroma")

def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


def build_vector_store(chunks):
    print(f"Building vector store from {len(chunks)} chunks...")
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    print(f"Vector store built and saved to {CHROMA_DIR}")
    return vector_store


def load_vector_store():
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
    return vector_store


if __name__ == "__main__":
    from src.ingestor import load_all_filings
    chunks = load_all_filings()
    build_vector_store(chunks)