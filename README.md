# CVM Reports RAG Q&A System

An advanced Question-Answering system using Retrieval-Augmented Generation (RAG) to unlock insights from the official management reports of the CVM (Brazilian Securities and Exchange Commission).

## About The Project

Navigating the dense, lengthy management reports from regulatory bodies like the CVM is a significant challenge for investors, analysts, and researchers. Finding specific information often requires hours of manual searching through complex PDF documents.

This project leverages a powerful multilingual Large Language Model (LLM) to transform this process. By indexing the CVM's annual reports into a vector database, this system allows users to ask complex questions in natural language (both English and Portuguese) and receive concise, accurate answers sourced directly from the documents.

This RAG pipeline effectively turns static, unstructured reports into a dynamic and interactive knowledge base.

### Key Features

* **Natural Language Queries:** Ask questions in plain English or Portuguese.
* **Source-Grounded Answers:** Responses are generated based on retrieved text chunks from the actual reports, minimizing hallucination and improving factual accuracy.
* **Multilingual Support:** Seamlessly handles queries and sources in both Portuguese and English thanks to a multilingual embedding model.
* **Complex Document Analysis:** Capable of synthesizing information from different sections or even across multiple reports to answer comparative and analytical questions.
* **Efficiency:** Drastically reduces the time required to find and analyze information within official regulatory filings.

## How It Works

The system follows a standard RAG pipeline:

1.  **Data Ingestion:** CVM management reports (PDFs) are loaded and parsed.
2.  **Chunking:** The extracted text is split into smaller, semantically coherent chunks.
3.  **Embedding & Indexing:** A multilingual sentence-transformer model generates vector embeddings for each chunk, which are then stored in a vector database (e.g., FAISS/ChromaDB).
4.  **Retrieval:** When a user asks a question, their query is embedded, and a similarity search retrieves the most relevant chunks from the database.
5.  **Generation:** The user's query and the retrieved context chunks are passed to a generative LLM, which formulates a comprehensive answer based on the provided information.

## Tech Stack

* **LLM Framework:** LangChain
* **LLM (Generator):** google/flan-t5-large
* **Embedding Model:** sentence-transformers/paraphrase-multilingual-mpnet-base-v2
* **Vector Database:** FAISS
* **Programming Language:** Python

---