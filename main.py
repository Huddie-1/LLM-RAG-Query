from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag_engine import get_answer
from mcp import generate_mcp
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import io
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_DIR = "rag_db"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    user_id: str = "anonymous"


@app.get("/")
def serve_ui():
    return FileResponse("ragstack_ui.html")


@app.post("/query")
def query_endpoint(query: QueryRequest):
    try:
        request_id = str(uuid.uuid4())
        answer, doc_ids = get_answer(query.question)
        mcp_payload = generate_mcp(
            request_id=request_id,
            user_id=query.user_id,
            query=query.question,
            doc_ids=doc_ids
        )
        return {
            "answer": answer,
            "sources": doc_ids,
            "metadata": mcp_payload
        }
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": [], "metadata": {}}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = content.decode("utf-8", errors="ignore")

        if not text.strip():
            return {"error": "File appears empty or unreadable"}

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        metadatas = [{"source": file.filename} for _ in chunks]

        vectordb.add_texts(chunks, metadatas=metadatas)

        return {
            "message": f"Successfully ingested {file.filename}",
            "chunks": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}