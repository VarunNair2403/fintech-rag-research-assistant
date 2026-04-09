# Fintech RAG Research Assistant

## The Problem

Financial analysts, product managers, and investors spend hours reading SEC 10-K filings to answer basic questions — what are a company's revenue streams, what risks do they face, how do two competitors compare. These documents are hundreds of pages long, dense with legal and financial language, and require significant domain expertise to interpret.

Tools like Bloomberg Terminal and AlphaSense charge thousands of dollars per seat to solve this problem. This project builds a lightweight version of that capability using RAG, LangChain, and GPT — demonstrating how AI can make financial research dramatically faster and more accessible.

---

## Why I Built This

The goal was to demonstrate:

- **RAG architecture** — the most important LLM pattern in enterprise AI today, used by every major AI product team
- **Fintech domain expertise** — working with real SEC filings, understanding revenue models, risk factors, and competitive dynamics
- **LangChain in production** — chunking, embedding, vector search, and retrieval all wired together end to end
- **Product thinking** — this maps directly to a $500M+ product category (AlphaSense, Kensho, Bloomberg AI)

This is the kind of internal tool a research analyst at a hedge fund or investment bank would use daily.

---

## How It Works

1. SEC 10-K PDFs are loaded and split into 1,000 character chunks with 200 character overlap via ingestor.py
2. Each chunk is embedded using OpenAI text-embedding-3-small and stored in a local Chroma vector store via embedder.py
3. When a question is asked, it is embedded and compared against all stored chunks using cosine similarity
4. The 5 most relevant chunks are retrieved and sent to GPT-4o-mini along with a structured prompt
5. GPT generates a cited answer referencing the specific company and filing section
6. cli.py or api.py delivers the response to the user

---

## Project Structure and File Explanations

**data/raw/** — Contains the raw SEC 10-K PDF filings. Currently includes PayPal FY2025 and Block FY2025 10-Ks. In production this would be populated by an automated SEC EDGAR ingestion pipeline.

**src/ingestor.py** — Loads PDFs using LangChain's PyPDFLoader and splits them into chunks using RecursiveCharacterTextSplitter. Chunk size of 1,000 characters with 200 character overlap ensures context is preserved across boundaries.

**src/embedder.py** — Converts document chunks into vector embeddings using OpenAI's text-embedding-3-small model and stores them in a local Chroma vector database. Also provides a load function to reload the vector store for querying.

**src/retriever.py** — Takes a natural language question, embeds it, retrieves the 5 most similar chunks from Chroma, and sends them to GPT-4o-mini with a financial analyst prompt. Returns the answer with source citations.

**src/cli.py** — Interactive terminal interface. Accepts questions in a loop and prints answers with sources. Type exit to quit.

**src/api.py** — FastAPI REST API with three endpoints: /health, /filings, and /ask. Makes the research assistant consumable by dashboards or other internal tools.

**.chroma/** — Local Chroma vector store directory. Contains all embeddings. Not committed to GitHub — regenerate by running python -m src.embedder.

---

## Quickstart (Local)

**1. Clone and set up environment**

```bash
git clone https://github.com/VarunNair2403/fintech-rag-research-assistant.git
cd fintech-rag-research-assistant
python3.11 -m venv .venv
source .venv/bin/activate
pip install langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters chromadb pypdf openai python-dotenv fastapi uvicorn
```

**2. Add your OpenAI key**

Create a .env file in the project root:

```env
OPENAI_API_KEY=sk-...
```

**3. Add 10-K filings**

Place PDF filings in data/raw/. Currently supports:
- paypal_10k_2025.pdf
- block_10k_2025.pdf

**4. Build the vector store**

```bash
python -m src.embedder
```

This embeds all PDFs and saves to .chroma/. Only needs to run once or when new filings are added.

**5. Run via CLI**

```bash
python -m src.cli
```

Example questions:
- What are the main risks PayPal faces?
- How does Block make money?
- Compare PayPal and Block's business models
- What is Block's Bitcoin revenue for 2025?

**6. Run via API**

```bash
uvicorn src.api:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

---

## API Endpoints

- GET /health — Service liveness check
- GET /filings — List all ingested 10-K filings
- POST /ask — Submit a question, returns answer with source citations

---

## Example Output

Question: How does Block make money?

Answer: Block generates revenue through three segments. Commerce Enablement Revenue from seller services was $11.5B in FY2025. Financial Solutions Revenue including Cash App was $4.2B. Bitcoin Ecosystem Revenue was $8.5B. (Source: block_10k_2025.pdf, Consolidated Statements of Operations)

---

## Taking This to Production

- **Data pipeline** — automate SEC EDGAR ingestion to pull new 10-K and 10-Q filings on a schedule
- **Vector store** — replace local Chroma with Pinecone or Weaviate for scalable multi-tenant search
- **Coverage** — expand beyond PayPal and Block to cover S&P 500 fintech companies
- **Reranking** — add a reranking step after retrieval to improve answer quality on complex questions
- **Streaming** — stream GPT responses token by token for a better user experience
- **Auth** — add user authentication so each analyst only accesses authorized filings
- **Hosting** — Dockerize and deploy on AWS ECS with the vector store on a managed service
- **Evaluation** — build a benchmark set of questions with known answers to measure RAG accuracy
- **Fine-tuning** — fine-tune embeddings on financial text for better retrieval precision

---

## Tech Stack

- Python 3.11+
- LangChain — document loading, chunking, retrieval pipeline
- Chroma — local vector store for embeddings
- OpenAI text-embedding-3-small — document and query embeddings
- OpenAI GPT-4o-mini — answer generation
- FastAPI + Uvicorn — REST API layer
- pypdf — PDF text extraction
- python-dotenv — environment config