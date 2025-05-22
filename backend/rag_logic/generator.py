from database.vector_db import VectorDB
from embeddings.text_embedder import TextEmbedder
from embeddings.image_embedder import ImageEmbedder
from memory.vector_memory import VectorMemory
from llm.response_generator import generate_response

text_embedder = TextEmbedder()
image_embedder = ImageEmbedder()
db = VectorDB(vector_size=512)
image_db = VectorDB(collection_name="image_embeddings", vector_size=512)
vector_memory = VectorMemory(db=db, embedder=text_embedder)


def generate_rag_response(query: str) -> dict:
    # Embed query
    query_embedding = text_embedder.embed([query])[0].tolist()

    # Retrieve relevant chat context
    chat_context = vector_memory.retrieve_relevant_chats(query)

    # Retrieve relevant articles
    article_hits = db.search_articles(query_embedding, top_k=3)
    article_context = []
    sources = []
    for article in article_hits:
        title = article.get("title", "Untitled")
        text = article.get("text", "")
        url = article.get("url", "")
        article_context.append(f"{title}: {text}\nSource: {url}")
        sources.append({"title": title, "url": url})

    # Combine context
    all_context = chat_context + article_context
    context_text = "\n".join(all_context) if all_context else ""

    # Generate response
    answer = generate_response(query=query, context_chunks=context_text)

    # Retrieve relevant images
    image_hits = image_db.search(
        embedding=query_embedding,
        top_k=2,
        type_="image"
    )
    images = [
        {
            "image_url": img.get("image_url"),
            "local_path": img.get("local_path"),
            "caption": img.get("caption")
        } for img in image_hits
    ]

    return {
        "answer": answer,
        "images": images,
        "sources": sources
    }