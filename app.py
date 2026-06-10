import streamlit as st
import os
import requests

from utils.pdf_loader import extract_text
from utils.chunker import chunk_text
from utils.embeddings import create_embeddings
from utils.vector_store import create_faiss
from utils.retriever import retrieve
from utils.llm import ask_llm

st.title("PDF RAG App")

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key or groq_api_key.startswith("gsk_your_"):
    st.warning(
        "Missing or placeholder Groq API key. Set GROQ_API_KEY in your .env to a valid key from the Groq dashboard."
    )


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    # PDF process only once
    if "index" not in st.session_state:
         os.makedirs("uploads", exist_ok=True)

    save_path = os.path.join(
        "uploads",
        uploaded_file.name
    )


    

    with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF..."):

            text = extract_text(save_path)
            print("Text Length:", len(text))


            chunks = chunk_text(text)
            print("Chunks Count:", len(chunks))

            embeddings = create_embeddings(chunks)

            index = create_faiss(embeddings)
            print("Index Size:", index.ntotal)

            st.session_state.index = index
            st.session_state.chunks = chunks

            st.success("PDF Processed Successfully")

    question = st.text_input(
        "Ask Question"
    )

    if st.button("Ask") and question:

        with st.spinner("Generating Answer..."):

            retrieved_chunks = retrieve(
                question,
                st.session_state.index,
                st.session_state.chunks
            )

            context = "\n".join(
                retrieved_chunks
            )

            try:
                answer = ask_llm(
                    question,
                    context
                )
            except ValueError as exc:
                st.error(str(exc))
                answer = None
            except requests.exceptions.RequestException as exc:
                st.error(f"Failed to call Groq API: {exc}")
                answer = None

        if answer:
            st.subheader("Answer")
            st.write(answer)