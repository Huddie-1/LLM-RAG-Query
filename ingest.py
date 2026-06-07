from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

texts = [
    "Retrieval-Augmented Generation (RAG) combines a retrieval system with a language model.",
    "ChromaDB is a vector database used to store and search document embeddings.",
    "LangChain is a framework for building applications powered by language models.",
    "Groq provides fast LLM inference using custom hardware called LPUs.",
]

metadatas = [
    {"source": "doc1"},
    {"source": "doc2"},
    {"source": "doc3"},
    {"source": "doc4"},
]

vectordb = Chroma.from_texts(
    texts, embeddings,
    metadatas=metadatas,
    persist_directory="rag_db"
)
print("Documents ingested successfully!")