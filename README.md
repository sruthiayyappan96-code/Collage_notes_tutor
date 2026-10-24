# 📚 StudyMate: College Notes Tutor (RAG Study Assistant)

An AI study assistant that answers your doubts and creates practice questions
**from your own notes PDF**, with page numbers for every answer.

**Live app:** <your-streamlit-link>
**Docker image:** `<your-dockerhub-username>/studymate-rag-assistant:1.0`

---

## Problem
Students waste time searching long notes before exams. Generic chatbots answer
from the internet, not from the student's own syllabus, and they can make up facts.

## Solution
The app uses **RAG (Retrieval-Augmented Generation)**. It first finds the most
relevant parts of your notes, then asks the AI to answer using only those parts.
Answers stay accurate and come with page references.

## Features
- Upload any text-based notes PDF
- Ask a doubt and get an answer based only on your notes
- See which pages were used
- Generate 5 exam-style practice questions (3 short, 2 long) on any topic
- Runs locally, in Docker, or on Streamlit Cloud
- Automated build and test with a Jenkins pipeline

## Tech Stack
| Tool | Use |
|---|---|
| Python | Main language |
| Streamlit | Web interface |
| PyPDF | Reading the PDF |
| FAISS | Vector database for similarity search |
| Gemini API | Embeddings and answer generation |
| NumPy | Handling vectors |
| Docker | Packaging the app |
| Jenkins | CI/CD pipeline |
| GitHub | Source code hosting |

## Project Structure
```
├── app.py              # all application code
├── requirements.txt    # Python packages
├── Dockerfile          # recipe to build the Docker image
├── .dockerignore       # files Docker should skip
├── Jenkinsfile         # CI/CD pipeline steps
├── .gitignore          # files Git should skip
├── sample_notes/       # sample PDF for testing
└── README.md
```

## How It Works
```
Notes PDF
   │
   ▼
Split into 150-word chunks (page number kept)
   │
   ▼
Convert chunks to vectors (embeddings)
   │
   ▼
Store in FAISS index

Your question → vector → FAISS finds the 4 closest chunks
                                   │
                                   ▼
          Gemini answers using only those chunks + page numbers
```

## Code Explanation
| Part | What it does |
|---|---|
| `MODEL`, `EMBED_MODEL`, `BACKUP_MODELS` | Model names in one place, so a rename is a one-line fix |
| `make_chunks()` | Cuts each page into 150-word pieces and keeps the page number |
| `embed()` | Turns text into vectors and normalizes them for cosine similarity |
| `faiss.IndexFlatIP` | The vector database that finds the closest chunks |
| `find_notes()` | Embeds the question and returns the top matching chunks |
| `ask_ai()` | Sends question and notes to Gemini. Retries 3 times, then tries a backup model on errors such as 503 |
| `st.session_state` | Remembers the index so the PDF is not processed on every click |


## Run Locally
```bash
git clone https://github.com/<your-github-username>/studymate-rag-assistant.git
cd studymate-rag-assistant
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```
Get a free API key at aistudio.google.com and paste it in the sidebar.
The key is never stored in the code.

*Paste your Gemini API key in the sidebar.
*Click Browse files and choose python_notes.pdf.
*Wait for “Reading your notes...” to finish.

What the notes cover
Unit	Topic
1	Introduction to Python
2	Data types and operators
3	Control statements and loops
4	Lists, tuples, sets, dictionaries
5	Functions and modules
6	Object oriented programming
7	File handling and exception handling
8	Python libraries for data science
Questions to test the app

In the Ask a doubt tab:

What is the difference between a list and a tuple?
What are the four pillars of OOP?
What does the break statement do?
How do I handle a FileNotFoundError?

In the Practice questions tab, type a topic like:

functions
dictionaries
exception handling

The answer should include page numbers, such as “Pages used: 3, 4”.

*Put the PDF in a sample_notes/ folder in your project, so recruiters can test your live app quickly.
*“Test the app with sample_notes/python_notes.pdf.”

Push it to GitHub:


## Run with Docker
```bash
docker build -t collage-notes-tutor .
docker run -p 8501:8501 collage-notes-tutor
```
Open http://localhost:8501

If port 8501 is busy, use another port:
```bash
docker run -p 8601:8601 collage-notes-tutor
```
Open http://localhost:8601

Or pull the ready-made image:
```bash
docker run -p 8501:8501 sruthivignesh/collage-notes-tutor:1.0
```

## CI/CD with Jenkins
Every push to GitHub can trigger this pipeline:

| Stage | What happens |
|---|---|
| Checkout | Jenkins downloads the latest code from GitHub |
| Build Docker Image | Runs `docker build` |
| Test | Runs a syntax check on `app.py` inside the container |
| Push to Docker Hub | Publishes the image using saved credentials |

The pipeline is defined in the `Jenkinsfile`.

## Configuration
| Setting | Where | Notes |
|---|---|---|
| Gemini API key | Sidebar input | Entered by the user, never saved |
| LLM model | `MODEL` in `app.py` | Currently `gemini-3.8-flash` |
| Embedding model | `EMBED_MODEL` in `app.py` | Currently `gemini-embedding-001` |

If you see a `404 model not found` error, check aistudio.google.com for the
current model name and update the variable.

## Sample Output
**Question:** What is normalization in DBMS?

**Answer:** Normalization is the process of organizing tables to reduce
duplicate data... *(Pages used: 12, 13)*

> Replace this with a real question and answer from your own notes.

## Limitations
- Works only with text PDFs (not scanned images)
- The index is rebuilt each time a new file is uploaded
- Free API tier has rate limits

## Future Improvements
- Support multiple PDFs at once
- Save the FAISS index to disk
- Add chat history
- Add a quiz mode that scores your answers
- Add automated unit tests to the Jenkins pipeline

## What I Learned
RAG, text chunking, embeddings, vector search with FAISS, prompt design to
reduce hallucination, containerizing with Docker, building a Jenkins CI/CD
pipeline, and deploying with GitHub and Streamlit Cloud.