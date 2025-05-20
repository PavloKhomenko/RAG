import streamlit as st
from database.vector_db import VectorDB
from embeddings.text_embedder import TextEmbedder
from embeddings.image_embedder import ImageEmbedder
from memory.vector_memory import VectorMemory
from llm.response_generator import generate_response
from data_ingestion.srcraper import BatchScraper


db = VectorDB(vector_size=512)
image_db = VectorDB(collection_name="image_embeddings", vector_size=512)
text_embedder = TextEmbedder()
image_embedder = ImageEmbedder()
vector_memory = VectorMemory(db=db, embedder=text_embedder)
batch_scraper = BatchScraper(text_embedder=text_embedder, image_embedder=image_embedder, text_db=db, image_db=image_db)

st.set_page_config(page_title="RAG System", layout="wide")

st.title("Multimodal RAG Assistant")
query = st.text_input("Ask your question:")

if st.button("Search") and query:

    with st.spinner("Retrieving results..."):
        # Embed query
        query_embedding = text_embedder.embed([query])[0].tolist()

        # Retrieve relevant memory (vector-based)
        chat_context = vector_memory.retrieve_relevant_chats(query)

        # Retrieve relevant articles
        article_hits = db.search_articles(query_embedding, top_k=3)
        article_context = []
        for article in article_hits:
            # You can adjust this to include more/less info
            title = article.get("title", "Untitled")
            text = article.get("text", "")
            url = article.get("url", "")
            article_context.append(f"{title}: {text}\nSource: {url}")

        # Combine chat and article context
        all_context = chat_context + article_context
        context_text = "\n".join(all_context) if all_context else ""

        # Generate response with retrieved context
        response = generate_response(query=query, context_chunks=context_text)

        image_hits = image_db.search(
            embedding=query_embedding,
            top_k=2,
            type_="image"
        )

        # Display result
        st.markdown(f"### 💬 Answer:\n{response}")
        if image_hits:
            st.markdown("### 🖼️ Relevant Images")
            cols = st.columns(2)
            for col, img in zip(cols, image_hits):
                img_src = img.get("image_url") or img.get("local_path")
                caption = img.get("caption", "")
                col.image(img_src, caption=caption, use_container_width=True)
        if article_hits:
            st.markdown("### 📚 Sources")
            for article in article_hits:
                title = article.get("title", "Untitled")
                url = article.get("url", None)
                if url:
                    st.markdown(f"- [{title}]({url})")
else:
    st.info("Enter a query and click 'Search' to see results.")

if st.button("Scrape Articles"):
    with st.spinner("Scraping articles..."):
        batch_scraper.run()
        st.success("Articles scraped and stored successfully!")

if st.button("Clear Chat History"):
    vector_memory.clear()
    st.success("Chat history cleared!")

        #TODO: Add README
        #TODO: Provide documentation
        #TODO: Add demo