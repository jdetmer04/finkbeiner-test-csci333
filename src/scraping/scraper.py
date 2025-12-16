import newspaper
from newspaper import Article
import json
from pathlib import Path

def scrape_article(url: str) -> dict:
    """Scrape a single article and return structured data."""
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    
    return {
        "url": url,
        "title": article.title,
        "text": article.text,
        "authors": article.authors,
        "publish_date": article.publish_date.isoformat() if article.publish_date else None,
        "keywords": article.keywords,
        "summary": article.summary
    }

def scrape_text(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    return article.text

if __name__ == "__main__":
    # this url for testing - (hopefully) not what's getting parsed if you run the main program
    test_url = "https://news.mit.edu/2011/timeline-richards-0126"
    data = scrape_article(test_url)
    
    # Save to data/raw/ with timestamp
    output_path = Path("data/raw/sample_article.json")
    output_path.write_text(json.dumps(data, indent=2))
    print(f"Saved to {output_path}")