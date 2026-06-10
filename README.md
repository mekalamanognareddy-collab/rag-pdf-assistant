# PDF RAG Assistant

## Overview

PDF RAG Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions in natural language. The system retrieves relevant information from the document and generates accurate responses using a Large Language Model.

## Features

* Upload PDF documents
* Extract text from PDFs
* Text chunking and preprocessing
* Semantic search using FAISS
* AI-powered question answering
* Streamlit-based user interface

## Tech Stack

* Python
* Streamlit
* FAISS
* Sentence Transformers
* Groq LLM

## Project Structure

rag-pdf-assistant/
├── app.py
├── utils/
├── uploads/
├── README.md
└── requirements.txt

## Installation

git clone <repository-url>

cd rag-pdf-assistant

pip install -r requirements.txt

streamlit run app.py

## Future Improvements

* Chat history
* Source citation display
* Cloud deployment
