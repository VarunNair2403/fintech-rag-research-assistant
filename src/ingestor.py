from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW_DIR = DATA_DIR / "raw"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_and_chunk(file_name: str):
    file_path = RAW_DIR / file_name
    print(f"Loading {file_path}...")

    loader = PyPDFLoader(str(file_path))
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {file_name}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def load_all_filings():
    all_chunks = []
    for pdf_file in RAW_DIR.glob("*.pdf"):
        chunks = load_and_chunk(pdf_file.name)
        all_chunks.extend(chunks)
    print(f"Total chunks across all filings: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    load_all_filings()