import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import Dict, List
from supabase import create_client

class PGEssayScraper:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.base_url = "http://www.paulgraham.com"
        self.articles_url = f"{self.base_url}/articles.html"
        self.supabase = create_client(supabase_url, supabase_key)

    def get_essay_links(self) -> List[Dict[str, str]]:
        response = requests.get(self.articles_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        essays = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.html') and href != 'articles.html':
                essays.append({
                    'title': link.text.strip(),
                    'url': f"{self.base_url}/{href}"
                })
        return essays

    def scrape_essay(self, url: str) -> Dict[str, str]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Most PG essays have the content in font tags
        content = ' '.join([p.text for p in soup.find_all('font')])
        
        # Clean the content
        content = re.sub(r'\s+', ' ', content).strip()
        
        return {
            'content': content,
            'scraped_at': datetime.utcnow().isoformat()
        }

    def store_essay(self, essay_data: Dict[str, str]):
        try:
            print("Storing essay:", essay_data['title'])
            if not essay_data['title'].strip():  # Skip empty titles
                print("Skipping essay with empty title")
                return
            
            result = self.supabase.table('essays').insert(essay_data).execute()
            print(f"Successfully stored: {essay_data['title']}")
            return result
        except Exception as e:
            print(f"Error storing essay: {str(e)}")
            return None

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    scraper = PGEssayScraper(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    essays = scraper.get_essay_links()
    for essay in essays:
        content = scraper.scrape_essay(essay['url'])
        essay_data = {**essay, **content}
        scraper.store_essay(essay_data)
        print(f"Stored: {essay['title']}")