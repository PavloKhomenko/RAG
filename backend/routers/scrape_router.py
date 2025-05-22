from fastapi import APIRouter
from data_ingestion.srcraper import BatchScraper
from embeddings.text_embedder import TextEmbedder
from embeddings.image_embedder import ImageEmbedder
from database.vector_db import VectorDB

router = APIRouter()

text_embedder = TextEmbedder()
image_embedder = ImageEmbedder()
db = VectorDB(vector_size=512)
image_db = VectorDB(collection_name="image_embeddings", vector_size=512)

scraper = BatchScraper(
    text_embedder=text_embedder,
    image_embedder=image_embedder,
    text_db=db,
    image_db=image_db
)

@router.post("/scrape")
async def scrape_articles():
    scraper.run()
    return {"detail": "Articles scraped and indexed."}