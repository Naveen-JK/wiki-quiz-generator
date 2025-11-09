import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scraper import WikipediaScraper

def test_scraper():
    scraper = WikipediaScraper()
    
    test_urls = [
        "https://en.wikipedia.org/wiki/Algorithm",
        "https://en.wikipedia.org/wiki/Artificial_intelligence", 
        "https://en.wikipedia.org/wiki/Computer_science"
    ]
    
    for url in test_urls:
        print(f"\n🧪 Testing URL: {url}")
        try:
            result = scraper.scrape_article(url)
            print(f"✅ Success! Title: {result['title']}")
            print(f"📝 Summary length: {len(result['summary'])}")
            print(f"📑 Sections: {len(result['sections'])}")
            print(f"📊 Content length: {len(result['content'])}")
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_scraper()