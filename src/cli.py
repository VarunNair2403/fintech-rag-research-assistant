from .retriever import ask


def main():
    print("\n=== Fintech RAG Research Assistant ===")
    print("Ask questions about PayPal and Block 10-K filings.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input(">> ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Goodbye.")
            break

        print("\nSearching filings...\n")
        response = ask(question)

        print(f"ANSWER:\n{response['answer']}\n")
        print(f"SOURCES: {response['sources']}\n")


if __name__ == "__main__":
    main()