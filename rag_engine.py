import os
from typing import Tuple, List
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

CHROMA_DB_DIR = "rag_db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
K_RETRIEVE = 3

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": K_RETRIEVE})
llm = ChatGroq(model_name=MODEL_NAME, temperature=0, groq_api_key=GROQ_API_KEY)


def get_answer(question: str) -> Tuple[str, List[str]]:
    try:
        relevant_docs = retriever.invoke(question)
        doc_ids = [doc.metadata.get("source", "unknown") for doc in relevant_docs]

        prompt_template = PromptTemplate.from_template(
            "Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt_template}
        )

        answer = qa_chain.invoke(question)["result"]
        return answer, doc_ids

    except Exception as e:
        return f"Error: {str(e)}", []