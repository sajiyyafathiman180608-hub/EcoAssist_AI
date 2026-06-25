import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv()


# ---------------- EMBEDDINGS ----------------
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ---------------- VECTOR DB ----------------
def get_vector_db():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory="eco_database",
        embedding_function=embeddings
    )


# ---------------- LLM ----------------
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=200,
        api_key=os.getenv("GROQ_API_KEY")
    )


# ---------------- MAIN FUNCTION ----------------
def ask_ecoassist(question: str):

    db = get_vector_db()
    llm = get_llm()

    docs = db.similarity_search(question, k=1)

    context = docs[0].page_content[:300] if docs else ""

    prompt = f"""
You are EcoAssist AI 🌱

Answer in 4-5 lines only.
Be simple and clear.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content


def clear_memory():
    pass
