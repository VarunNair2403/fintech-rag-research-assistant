from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

from .embedder import load_vector_store

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

PROMPT_TEMPLATE = """
You are a financial analyst assistant specializing in fintech companies.
Use the following excerpts from SEC 10-K filings to answer the question.
Always cite which company and section your answer comes from.
If you don't know the answer from the provided context, say so clearly.

Context:
{context}

Question: {question}

Answer:
"""


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_sources(docs):
    return list(set([
        doc.metadata.get("source", "unknown").split("/")[-1]
        for doc in docs
    ]))


def ask(question: str) -> dict:
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    retrieved_docs = retriever.invoke(question)
    context = format_docs(retrieved_docs)
    sources = get_sources(retrieved_docs)

    formatted_prompt = prompt.format(context=context, question=question)
    answer = llm.invoke(formatted_prompt).content

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    response = ask("What is PayPal's total revenue for 2025?")
    print("\nQUESTION:", response["question"])
    print("\nANSWER:", response["answer"])
    print("\nSOURCES:", response["sources"])