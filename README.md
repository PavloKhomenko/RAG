# Multimodal RAG Assistant

This project is a Multimodal Retrieval-Augmented Generation (RAG) system for advanced question answering. It supports text and image retrieval, chat memory, and web article ingestion for enhanced LLM-based responses. The stack includes a FastAPI backend, React frontend, and Qdrant vector database, all orchestrated via Docker Compose.

---

## Features

- **Multimodal RAG:** Combines chat, articles, and images for context-rich answers.
- **Web Scraping:** Scrape and chunk articles from [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/).
- **Image Embeddings:** Store and retrieve relevant images using CLIP.
- **Text Embeddings:** CLIP-based unified vector space for text and image alignment.
- **Chat Memory:** Vector-based chat history for persistent context.
- **Evaluation:** RAGAS-based evaluation pipeline with metrics like faithfulness, answer relevancy, and context precision.

---

## Architecture Overview

1. **User Input:** A question is submitted via the React frontend.
2. **Text Embedding:** The question is embedded using CLIP (ViT-B-32).
3. **Vector Search:** Contextual chunks and image embeddings are retrieved from Qdrant.
4. **LLM Generation:** The query and context are passed to an OpenAI LLM (GPT-4o).
5. **Response Display:** The answer is shown alongside relevant images and article sources.

---

## Technology Stack

| Component       | Tool/Library            | Reason for Selection                     |
| --------------- | ----------------------- | ---------------------------------------- |
| LLM             | OpenAI GPT-4o           | High-quality natural language generation |
| Text Embedding  | open-clip (ViT-B-32)    | Shared space for text & images           |
| Image Embedding | open-clip (ViT-B-32)    | Unified vision-language embedding        |
| Vector Storage  | Qdrant                  | Fast vector DB with payload filtering    |
| Backend API     | FastAPI                 | Modern, async Python API framework       |
| Frontend        | React + Vite            | Fast, modern web UI                      |
| Evaluation      | RAGAS                   | Specialized tool for RAG quality metrics |
| Scraping        | BeautifulSoup, requests | Flexible HTML content extraction         |
| Orchestration   | Docker Compose          | Easy multi-service deployment            |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd RAG
```

### 2. Configure Environment Variables

Create a `.env` file in `backend/`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Build and Start All Services

Make sure [Docker](https://www.docker.com/products/docker-desktop/) is installed and running.

```bash
docker-compose up --build
```

- **Qdrant** will be available at `localhost:6333`
- **Backend API** at `localhost:8000`
- **Frontend** at `localhost:5173`

### 4. (Optional) Manual Python Environment

If you want to run backend or evaluation scripts outside Docker:

```bash
python3.11 -m venv venv311
source venv311/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

---

## Usage

### 1. Web Interface

Open [http://localhost:5173](http://localhost:5173) in your browser.

- Enter a query and click **Search** to receive context-grounded answers.
- Click **Scrape Articles** to ingest latest content from The Batch.
- Click **Clear Chat History** to reset memory in the current session.

### 2. API Endpoints

- `POST /api/query` — Ask a question.
- `POST /api/scrape` — Scrape and ingest new articles.
- `POST /api/clear` — Clear chat memory.

### 3. Evaluate RAG Performance

Run the following command (in the root or backend directory):

```bash
python evaluation/metrics.py
```

Make sure your `evaluation/rag_samples.jsonl` contains entries like:

```json
{
  "question": "What is CLIP?",
  "contexts": ["CLIP is a neural network trained on image-text pairs."],
  "answer": "CLIP is a model that connects images and texts.",
  "reference": "CLIP is a model trained on image-text pairs to learn a shared embedding space."
}
```

---

## Evaluation Metrics

- **Faithfulness:** Is the answer actually supported by the retrieved context?
- **Answer Relevancy:** Is the answer on-topic with respect to the question?
- **Context Precision:** Do the retrieved contexts actually help answer the question? *(requires reference)*

RAGAS uses LLM-as-a-judge (e.g., GPT-4) to rate each sample.

---

## Design Decisions

- **CLIP** for both text and image embeddings enables unified retrieval.
- **Qdrant** provides fast approximate search and supports metadata-rich queries.
- **open-clip** enables modern ViT-based CLIP variants with shared embedding spaces.
- **FastAPI** for a modern, async backend.
- **React** and **Vite** for a fast, modern frontend.
- **RAGAS** for standardized, explainable evaluation of retrieval+generation.

---

## Future Improvements

- Add inline citations inside generated answers.
- Add support for PDF ingestion and parsing.
- Track chat history per session/user with timestamps.
- Visualize context contribution heatmaps in UI.

---

## Troubleshooting

- **Segmentation Faults:** Ensure compatible versions of PyTorch and OpenCLIP are installed.
- **Empty Qdrant results:** Make sure articles are scraped and vectorized properly.
- **Evaluation errors:** Add a `reference` field if using context-related metrics like `context_precision`.
- **Docker issues:** Make sure Docker Desktop is running and ports 5173, 8000, and 6333 are free.

---

**Enjoy your Multimodal RAG Assistant!**