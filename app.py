import faiss
import numpy as np
import streamlit as st
from google import genai
from pypdf import PdfReader
import time
from google.genai import errors

EMBED_MODEL = "gemini-embedding-001"
MODEL = "gemini-3.8-flash"   # if Google changes the name, fix it here only
BACKUP_MODELS = ["gemini-flash-latest"]   # tried if the main model is busy

st.title("📚 College Notes Tutor")
key = st.sidebar.text_input("Gemini API key", type="password")
pdf = st.file_uploader("Upload your notes (PDF)", type="pdf")

if not (key and pdf):
    st.info("Enter your API key and upload a notes PDF.")
    st.stop()

client = genai.Client(api_key=key)


def embed(texts):
    """Text -> numbers (vectors)."""
    out = []
    for i in range(0, len(texts), 50):
        r = client.models.embed_content(
            model=EMBED_MODEL, contents=texts[i:i + 50])
        out += [e.values for e in r.embeddings]
    vectors = np.array(out, dtype="float32")
    faiss.normalize_L2(vectors)
    return vectors


def make_chunks(reader, size=150):
    """Cut every page into small pieces of 150 words (page number is kept)."""
    chunks = []
    for page_no, page in enumerate(reader.pages, 1):
        words = (page.extract_text() or "").split()
        for i in range(0, len(words), size):
            chunks.append((page_no, " ".join(words[i:i + size])))
    return chunks


def ask_ai(prompt):
    """Try the main model 3 times, then the backup models."""
    for model in [MODEL] + BACKUP_MODELS:
        for attempt in range(3):
            try:
                return client.models.generate_content(
                    model=model, contents=prompt).text
            except errors.APIError:
                time.sleep(2 * (attempt + 1))  # wait 2s, 4s, 6s
    return "The AI service is busy right now. Please try again in a minute."


def find_notes(question, n=4):
    """Search FAISS for the most relevant note pieces."""
    _, ids = index.search(embed([question]), min(n, len(chunks)))
    return [chunks[i] for i in ids[0]]


# Build the vector database once per uploaded file
if st.session_state.get("file") != pdf.name:
    with st.spinner("Reading your notes..."):
        chunks = make_chunks(PdfReader(pdf))
        if not chunks:
            st.error("No text found. Use a text PDF, not a scanned image.")
            st.stop()
        vectors = embed([text for _, text in chunks])
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        st.session_state.update(file=pdf.name, chunks=chunks, index=index)

chunks = st.session_state["chunks"]
index = st.session_state["index"]

tab1, tab2 = st.tabs(["Ask a doubt", "Practice questions"])

with tab1:
    question = st.text_input("Your doubt")
    if question:
        found = find_notes(question)
        context = "\n\n".join(f"[Page {p}] {t}" for p, t in found)
        st.write(ask_ai(
            f"Answer the question using only these notes. Mention page numbers.\n\n"
            f"Notes:\n{context}\n\nQuestion: {question}"))
        pages = sorted({p for p, _ in found})
        st.caption("Pages used: " + ", ".join(map(str, pages)))

with tab2:
    topic = st.text_input("Topic for practice questions")
    if st.button("Generate"):
        found = find_notes(topic, n=6)
        context = "\n\n".join(t for _, t in found)
        st.write(ask_ai(
            f"From these notes, write 5 exam questions on '{topic}' "
            f"(3 short answer, 2 long answer) with answers.\n\nNotes:\n{context}"))