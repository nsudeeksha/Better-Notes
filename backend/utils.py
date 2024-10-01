import fitz  # PyMuPDF for PDF text extraction
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.getenv('openai_key')

client = OpenAI(api_key=openai_key)
import pinecone

# 1. Extract text from PDF
def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 2. Generate embedding using OpenAI's API
def get_embedding(text):
    response = client.embeddings.create(input=text,
    model="text-embedding-ada-002")
    return response.data[0].embedding

# 3. Search Pinecone for relevant chunks based on input notes
def search_relevant_chunks(notes, pinecone_index):
    # Get embedding for the notes
    notes_embedding = get_embedding(notes)

    # Query Pinecone index for top-k relevant chunks
    response = pinecone_index.query(
        vector=notes_embedding,
        top_k=5,
        include_metadata=True
    )

    # Extract and return relevant chunks
    return [match['metadata']['chunk_text'] for match in response.matches]

# 4. Enhance notes using OpenAI GPT-4
def enhance_notes_with_gpt(notes, relevant_chunks):
    try:
        prompt = (
            f"Given the following notes:\n{notes}\n\n"
            f"And the relevant textbook content:\n{relevant_chunks}\n\n"
            "Improve the coherence, clarity, and content of the notes without over rewriting."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that helps improve the clarity and coherence of notes. Try not to over write. Generate the notes in an aesthetically-pleasing HTML format"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # Ensure the response has choices
        if response:
            print(response.choices[0].message.content)
            return response.choices[0].message.content
    except Exception as e:
        print(f"Error enhancing notes with GPT: {e}")
        return ""
