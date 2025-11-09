import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class WikipediaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url: str):
        """Simple and reliable Wikipedia scraping"""
        try:
            print(f"🔍 Scraping: {url}")
            
            # Validate URL
            if not self._is_valid_wikipedia_url(url):
                raise ValueError("Invalid Wikipedia URL")
            
            # Get the page
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # SIMPLE TITLE EXTRACTION
            title = self._get_simple_title(soup, url)
            print(f"📖 Title: {title}")
            
            # SIMPLE CONTENT EXTRACTION - Just get all text
            all_text = soup.get_text()
            cleaned_text = self._clean_text(all_text)
            
            # Create summary (first 500 chars)
            summary = cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
            
            # Use first 3000 chars for AI processing
            content = cleaned_text[:3000]
            
            # Simple sections extraction
            sections = self._get_simple_sections(soup)
            
            print(f"✅ Success! Content: {len(content)} chars, Sections: {len(sections)}")
            
            return {
                "title": title,
                "summary": summary,
                "sections": sections,
                "key_entities": {"people": [], "organizations": [], "locations": []},
                "content": content,
                "raw_html": str(soup)
            }
            
        except Exception as e:
            print(f"❌ Scraping error: {e}")
            raise Exception(f"Scraping failed: {str(e)}")
    
    def _is_valid_wikipedia_url(self, url: str) -> bool:
        """Validate Wikipedia URL"""
        try:
            parsed = urlparse(url)
            return ('wikipedia.org' in parsed.netloc and 
                   '/wiki/' in parsed.path)
        except:
            return False
    
    def _get_simple_title(self, soup, url):
        """Get title with multiple fallbacks"""
        # Try multiple title selectors
        selectors = [
            'h1.firstHeading',
            'h1#firstHeading', 
            'h1',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                title = element.get_text().strip()
                # Clean the title
                title = re.sub(r' - Wikipedia$', '', title)
                title = re.sub(r'\[edit\]', '', title)
                if title and title != "Wikipedia":
                    return title
        
        # Fallback: Extract from URL
        title_from_url = url.split('/')[-1].replace('_', ' ').title()
        return title_from_url if title_from_url else "Wikipedia Article"
    
    def _get_simple_sections(self, soup):
        """Get section headings simply"""
        sections = []
        headings = soup.find_all(['h2', 'h3', 'h4'])
        
        for heading in headings[:10]:  # Limit to first 10 headings
            text = heading.get_text().strip()
            text = re.sub(r'\[edit\]', '', text)
            text = re.sub(r'\[.*?\]', '', text)
            text = text.strip()
            
            # Skip unwanted sections
            skip_keywords = ['contents', 'navigation', 'menu', 'references', 'external links', 'see also', 'footnotes']
            if (text and 
                len(text) > 2 and 
                not any(keyword in text.lower() for keyword in skip_keywords)):
                sections.append(text)
        
        return sections if sections else ["Main Content"]
    
    def _clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove citation markers like [1], [2]
        text = re.sub(r'\[\d+\]', '', text)
        # Remove edit markers
        text = re.sub(r'\[edit\]', '', text)
        
        return text.strip()