import os
import requests
from bs4 import BeautifulSoup
import textwrap
from urllib.parse import urljoin, urlparse

class BatchScraper:
    def __init__(self, text_embedder, image_embedder, text_db, image_db, base_url="https://www.deeplearning.ai/the-batch/", image_folder="images"):
        self.text_embedder = text_embedder
        self.image_embedder = image_embedder
        self.text_db = text_db
        self.image_db = image_db
        self.base_url = base_url
        self.image_folder = image_folder
        os.makedirs(self.image_folder, exist_ok=True)

    def get_article_links(self):
        resp = requests.get(self.base_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        links = []
        for a in soup.select('a[href*="/the-batch/"]'):
            href = a.get('href')
            if href and '/the-batch/' in href and href != '/the-batch/':
                full_url = urljoin(self.base_url, href)
                if full_url not in links:
                    links.append(full_url)
        return links

    def download_image(self, img_url):
        filename = os.path.basename(urlparse(img_url).path)
        filepath = os.path.join(self.image_folder, filename)
        try:
            img_data = requests.get(img_url).content
            with open(filepath, 'wb') as f:
                f.write(img_data)
            return filepath
        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")
            return None

    def scrape_article(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        article = soup.find('article') or soup.find('main')
        text = article.get_text(separator='\n', strip=True) if article else ""

        images = []
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url and img_url.startswith('http'):
                local_path = self.download_image(img_url)
                if local_path:
                    images.append({
                        'url': img_url,
                        'local_path': local_path
                    })

        return {
            'title': title,
            'url': url,
            'text': text,
            'images': images
        }

    def process_article(self, article_data, chunk_size=1000):
        title = article_data["title"]
        text = article_data["text"]
        url = article_data["url"]

        if len(text.strip()) < 100:
            print(f"⚠️ Skipping short article: {title}")
            return

        # 🔹 Розбити текст на шматки
        chunks = textwrap.wrap(text, width=chunk_size, break_long_words=False)

        for idx, chunk in enumerate(chunks):
            chunk_title = f"{title} [Part {idx + 1}/{len(chunks)}]" if len(chunks) > 1 else title
            text_embedding = self.text_embedder.embed([chunk])[0].tolist()

            self.text_db.add_embedding(
                type_="article",
                embedding=text_embedding,
                title=chunk_title,
                text=chunk,
                url=url,
                date=None,
                chunk_id=idx,
                chunk_total=len(chunks)
            )

        print(f"✅ Stored article in {len(chunks)} chunk(s): {title}")

        # 2. Embed and store images
        for img in article_data["images"]:
            local_path = img["local_path"]
            try:
                image_embedding = self.image_embedder.embed_image(local_path)  # assumes filepath input
                self.image_db.add_embedding(
                    type_="image",
                    embedding=image_embedding,
                    image_url=img["url"],
                    caption=f"Image from: {title}"
                )
            except Exception as e:
                print(f"❌ Image embedding failed for {local_path}: {e}")

        print(f"✅ Stored article: {title}")

    def run(self):
        links = self.get_article_links()
        print(f"🌐 Found {len(links)} articles.")
        for link in links:
            try:
                article = self.scrape_article(link)
                self.process_article(article)
            except Exception as e:
                print(f"❌ Error processing {link}: {e}")
        print("✅ Scraping completed.")


