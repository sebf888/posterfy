import requests
from bs4 import BeautifulSoup
from ..config import WIKI_API_URL

def get_wikipedia_album_description(album_name: str, artist_name: str) -> str:
    """Fetch album description from Wikipedia."""
    search_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': f'intitle:{album_name} {artist_name}',
        'srlimit': 1
    }
    
    response = requests.get(WIKI_API_URL, params=search_params)
    results = response.json()['query']['search']
    
    if results:
        page_title = results[0]['title']
        content_params = {
            'action': 'parse',
            'format': 'json',
            'page': page_title,
            'prop': 'text',
            'section': 0
        }
        
        response = requests.get(WIKI_API_URL, params=content_params)
        html_content = response.json()['parse']['text']['*']
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for sup in soup('sup'):
            sup.decompose()
            
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            if p.text.strip():
                return ' '.join(p.text.strip().split())
    
    return " "