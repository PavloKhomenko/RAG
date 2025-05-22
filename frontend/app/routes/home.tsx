import React, { useState } from 'react';
import Spinner from '../components/Spinner';

function QueryPage() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [images, setImages] = useState<any[]>([]);
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setAnswer('');
    setImages([]);
    setSources([]);

    try {
      const res = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setAnswer(data.answer);
      setImages(data.images || []);
      setSources(data.sources || []);
    } catch (error) {
      console.error('Failed to fetch:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/scrape', {
        method: 'POST'
      });
      const data = await res.json();
      alert(data.detail || 'Scraping complete');
    } catch (error) {
      console.error('Failed to scrape articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/clear', {
        method: 'POST'
      });
      const data = await res.json();
      alert(data.detail || 'Chat history cleared');
    } catch (error) {
      console.error('Failed to clear history:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h1>Multimodal RAG Assistant</h1>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask your question..."
          style={{ flex: 1, padding: '0.5rem' }}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Processing...' : 'Search'}
        </button>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <button onClick={handleScrape} disabled={loading}>Scrape Articles</button>
        <button onClick={handleClearHistory} disabled={loading}>Clear Chat History</button>
      </div>
      {loading && <Spinner />}

      {answer && (
        <div>
          <h2>💬 Answer</h2>
          <p>{answer}</p>
        </div>
      )}

      {images.length > 0 && (
        <div style={{ marginTop: '1rem' }}>
          <h3>🖼️ Relevant Images</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
            {images.map((img, index) => (
              <img
                key={index}
                src={img.image_url || img.local_path}
                alt={img.caption || 'Relevant image'}
                style={{ width: '300px', borderRadius: '8px' }}
              />
            ))}
          </div>
        </div>
      )}

      {sources.length > 0 && (
        <div style={{ marginTop: '1rem' }}>
          <h3>📚 Sources</h3>
          <ul>
            {sources.map((src, index) => (
              <li key={index}>
                <a href={src.url} target="_blank" rel="noreferrer">
                  {src.title || src.url}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default QueryPage;