# PRD: Fintech RAG Research Assistant

**Author:** Varun Nair
**Status:** v1.0 — Complete
**Last Updated:** April 2026

---

## Problem Statement

SEC 10-K filings are the most comprehensive source of truth about a public company's business model, financial performance, risk factors, and competitive position. Every investment decision, competitive analysis, and product strategy at a financial institution is informed by this data.

The problem is accessibility. A single 10-K filing can be 300-500 pages of dense legal and financial language. Extracting specific answers requires either hours of manual reading or expensive specialized tools. Bloomberg Terminal costs $25,000 per seat per year. AlphaSense costs $50,000+ per year. Neither is accessible to most product teams, analysts, or developers building fintech products.

Large language models change this equation. RAG (Retrieval Augmented Generation) makes it possible to build a system that answers specific questions over large document corpora accurately, with citations, in seconds. This project demonstrates that capability over real SEC filings.

---

## Target Users

- **Equity research analysts** — need to extract specific financial metrics and risk factors from filings quickly
- **Fintech product managers** — need competitive intelligence on how rivals generate revenue and what risks they disclose
- **Investment associates** — need to compare business models and financial performance across companies
- **Developers building fintech products** — need to understand regulatory and compliance language in filings
- **Internal strategy teams** — need on-demand answers from financial documents without reading hundreds of pages

---

## Goals

**Primary Goals**
- Answer natural language questions over SEC 10-K filings accurately with source citations
- Retrieve the most relevant passages from large document corpora using semantic similarity search
- Generate answers that feel like they came from a financial analyst — specific, cited, and honest about uncertainty

**Secondary Goals**
- Build a reusable RAG architecture that can be extended to any document corpus
- Expose the research assistant as a REST API for integration into internal tools
- Demonstrate a production-ready pattern for LLM-augmented financial research

**Non-Goals for v1**
- Real-time ingestion of new SEC filings
- Coverage beyond PayPal and Block 10-Ks
- Multi-user authentication and access control
- Fine-tuning embeddings on financial text
- Streaming responses

---

## Success Metrics

- **Answer accuracy** — responses correctly reference data from the actual filing, not hallucinated figures
- **Citation quality** — every answer includes the source document and section
- **Honest uncertainty** — system says it does not know when the retrieved chunks do not contain the answer
- **Retrieval relevance** — top 5 retrieved chunks contain information relevant to the question
- **API response time** — /ask endpoint returns in under 8 seconds including embedding and LLM call

---

## Scope — What Is In v1

- PDF ingestion via LangChain PyPDFLoader
- Recursive text chunking at 1,000 characters with 200 character overlap
- OpenAI text-embedding-3-small embeddings stored in local Chroma vector store
- Similarity search retrieving top 5 most relevant chunks per question
- GPT-4o-mini answer generation with financial analyst system prompt
- Source citation in every response
- CLI with interactive question loop
- FastAPI REST API with /health, /filings, and /ask endpoints
- Coverage: PayPal FY2025 10-K and Block FY2025 10-K

## Scope — What Is Out of v1

- Automated SEC EDGAR ingestion pipeline
- Coverage beyond two filings
- Reranking of retrieved chunks
- Multi-user authentication
- Persistent query history
- Streaming responses
- Fine-tuned embeddings
- Frontend UI

---

## Feature Breakdown

**1. Document Ingestion (ingestor.py)**
Loads SEC 10-K PDFs using LangChain's PyPDFLoader which extracts text page by page. Splits documents into chunks using RecursiveCharacterTextSplitter with a chunk size of 1,000 characters and 200 character overlap. The overlap ensures that context is not lost at chunk boundaries — critical for financial data where numbers and their descriptions may span multiple paragraphs.

**2. Embedding and Vector Store (embedder.py)**
Converts all document chunks into dense vector representations using OpenAI's text-embedding-3-small model. Stores all vectors in a local Chroma database that persists to disk. When a new question arrives, it is embedded using the same model and compared against all stored vectors using cosine similarity to find the most semantically relevant chunks.

**3. Retrieval and Answer Generation (retriever.py)**
Retrieves the top 5 most similar chunks for a given question. Formats them into a context block and sends to GPT-4o-mini with a system prompt instructing it to act as a financial analyst, cite sources, and admit uncertainty when the context does not contain the answer. Returns the answer and a deduplicated list of source documents.

**4. CLI (cli.py)**
Interactive terminal interface with a continuous question loop. Prints answers and sources after each query. Type exit to quit. Suitable for local analyst use or batch question processing.

**5. REST API (api.py)**
Three endpoints via FastAPI. GET /health for liveness. GET /filings lists all ingested PDF files. POST /ask accepts a question and returns the answer, sources, and timestamp.

---

## Technical Architecture

Data flows in one direction:

PDF files → ingestor.py → text chunks → embedder.py → OpenAI embeddings API → Chroma vector store → retriever.py → similarity search → top 5 chunks + question → GPT-4o-mini → cited answer → cli.py or api.py → output

Stack: Python 3.11+, LangChain, Chroma, OpenAI text-embedding-3-small, OpenAI GPT-4o-mini, FastAPI, Uvicorn, pypdf, python-dotenv

---

## Production Roadmap

- **Data pipeline** — automated SEC EDGAR watcher that ingests new 10-K and 10-Q filings within 24 hours of publication
- **Vector store** — replace local Chroma with Pinecone or Weaviate for scalable multi-tenant vector search
- **Coverage** — expand to all S&P 500 fintech and financial services companies
- **Reranking** — add a cross-encoder reranking step after retrieval to improve answer quality on ambiguous questions
- **Hybrid search** — combine semantic similarity with keyword search (BM25) for better recall on specific financial figures
- **Streaming** — stream GPT responses token by token for better perceived performance
- **Auth** — OAuth2 so analysts only access filings they are authorized to query
- **Query history** — log all questions and answers per user for audit and review
- **Evaluation** — benchmark set of 50 questions with known answers to measure RAG accuracy and regression test on model updates
- **Fine-tuning** — fine-tune embedding model on financial text corpus for higher retrieval precision
- **Hosting** — Docker container on AWS ECS with Pinecone as managed vector store and RDS for query history

---

## Open Questions

1. Should chunk size be tuned per document type — smaller for financial tables, larger for narrative sections?
2. Should the system support multi-document queries that explicitly compare two filings side by side?
3. At what corpus size does local Chroma need to be replaced with a managed vector database?
4. Should retrieved chunks be reranked before being sent to the LLM to improve answer quality?
5. How should the system handle questions about specific financial figures that may appear in tables rather than prose?