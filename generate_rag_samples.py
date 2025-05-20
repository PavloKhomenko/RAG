import json
from database.vector_db import VectorDB
from embeddings.text_embedder import TextEmbedder
from llm.response_generator import generate_response
from tqdm import tqdm

db = VectorDB(vector_size=512)
text_embedder = TextEmbedder()

questions = [
    "What is CLIP?",
    "How does Qdrant store data?",
    "What is Retrieval-Augmented Generation?",
    "What are diffusion models?",
    "What is the role of transformers in neural networks?",
    "How is multimodal learning useful?"
]

output_path = "evaluation/rag_samples.jsonl"

def run_rag_pipeline(question):
    query_embedding = text_embedder.embed(question)
    chunks = db.search(query_embedding)

    context_texts = [chunk["text"] for chunk in chunks]
    answer = generate_response(question, context_texts)

    return {
        "question": question,
        "contexts": context_texts,
        "answer": answer
    }

def main():
    print("⚙️ Generating RAG samples...")
    results = []

    for q in tqdm(questions):
        result = run_rag_pipeline(q)
        results.append(result)

    print(f"💾 Saving results to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("✅ Done.")

if __name__ == "__main__":
    main()
