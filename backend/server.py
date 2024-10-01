from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from pinecone import Pinecone, ServerlessSpec
from utils import extract_text_from_pdf, get_embedding, search_relevant_chunks, enhance_notes_with_gpt
import markdown2
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
pinecone_key = os.getenv('pinecone_key')


# FastAPI app
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI and Pinecone
pc = Pinecone(api_key=pinecone_key)
index = pc.Index("textbook-embeddings")
print(index.describe_index_stats())

# Request model for note submission
class NotesRequest(BaseModel):
    notes: str


@app.post("/upload/")
async def upload_textbook_and_notes(
    textbook: UploadFile = File(...), notes: str = Form(...)
):
    # Step 1: Extract text from uploaded PDF textbook
    textbook_text = extract_text_from_pdf(await textbook.read())

    # Step 2: Generate embeddings for the textbook
    chunks = [textbook_text[i:i + 500] for i in range(0, len(textbook_text), 500)]
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        # Upsert chunk embeddings into Pinecone
        index.upsert([(f"chunk_{i}", embedding, {"chunk_text": chunk})])

    # Step 3: Enhance notes using relevant textbook content
    enhanced_notes = await process_notes(notes)

    return {"enhanced_notes": enhanced_notes}


@app.post("/process/")
async def process_notes(request: NotesRequest):
    notes=request.notes
    # Step 1: Get relevant sections from Pinecone
    relevant_chunks = search_relevant_chunks(notes, index)

    # Step 2: Use GPT-4 to enhance the notes
    enhanced_notes = enhance_notes_with_gpt(notes, relevant_chunks)

    return enhanced_notes
