from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

# Load environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
GELATO_API_KEY = os.getenv('GELATO_API_KEY')
GELATO_STORE_ID = os.getenv('GELATO_STORE_ID')
SAVE_DIRECTORY = os.getenv('SAVE_DIRECTORY')

