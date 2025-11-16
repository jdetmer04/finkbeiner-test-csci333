from src.scraping.scraper import scrape_article
from src.processing.text_cleaner import extract_scientist_info, flag_baseline_phrases
import json

def main():
    # 1. Scrape
    url = "https://news.mit.edu/2011/timeline-richards-0126"
    article_data = scrape_article(url)
    
    # 2. Process
    scientist_info = extract_scientist_info(article_data["text"])
    flags = flag_baseline_phrases(article_data["text"])
    
    # 3. Save processed version
    processed = {
        **article_data,
        "scientist_info": scientist_info,
        "bias_flags": flags
    }
    
    with open("data/processed/sample_processed.json", "w") as f:
        json.dump(processed, f, indent=2)
    
    print(f"Found {len(flags)} potential violations")
    print(f"Potential scientists: {scientist_info['potential_scientists']}")

if __name__ == "__main__":
    main()