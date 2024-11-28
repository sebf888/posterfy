import os
import requests
from typing import List, Tuple
from src.api.spotify import get_spotify_access_token, fetch_spotify_album_data
from src.api.wikipedia import get_wikipedia_album_description
from src.api.imgur import upload_to_imgur
from src.api.gelato import upload_to_gelato
from src.image_processing.poster import create_alternate_poster
from src.utils.helpers import sanitize_filename, ensure_directory_exists
from src.config import SAVE_DIRECTORY

def process_album(album_name: str, artist_name: str, access_token: str) -> None:
    """Process a single album to create and upload a poster."""
    try:
        print(f"\nProcessing '{album_name}' by '{artist_name}'")
        
        # Fetch album data and description
        album_data = fetch_spotify_album_data(album_name, artist_name, access_token)
        description = get_wikipedia_album_description(album_name, artist_name)
        
        # Get album cover URL
        album_cover_url = album_data['images'][0]['url']
        
        # Create save directory if it doesn't exist
        ensure_directory_exists(SAVE_DIRECTORY)
        
        # Download the image
        filename = sanitize_filename(f"{album_name} - {artist_name}.png")
        full_path = os.path.join(SAVE_DIRECTORY, filename)
        
        # Download image
        response = requests.get(album_cover_url, stream=True)
        if response.status_code == 200:
            with open(full_path, 'wb') as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)
            print(f"Album cover downloaded successfully")
        else:
            raise Exception(f"Failed to download album cover. Status code: {response.status_code}")
        
        # Create and save poster
        poster = create_alternate_poster(album_name, artist_name, description, full_path)
        poster_save_path = os.path.join(SAVE_DIRECTORY, 
                                      sanitize_filename(f"{album_name} - {artist_name} Poster.jpg"))
        poster.save(poster_save_path, format='JPEG')
        print(f"Poster saved: {poster_save_path}")
        
        # Upload to Imgur
        poster_public_url = upload_to_imgur(poster_save_path)
        print("Poster uploaded to Imgur")
        
        # Create Gelato listing
        gelato_response = upload_to_gelato(poster_public_url, album_name, artist_name)
        print("Poster listed on Gelato")
        
    except Exception as e:
        print(f"Error processing {album_name} by {artist_name}: {str(e)}")

def get_album_input() -> List[Tuple[str, str]]:
    """Get album and artist names from user input."""
    print("Enter album and artist names (tab-separated), type 'aa' when done:")
    input_lines = []
    while True:
        input_text = input().strip()
        if input_text.lower() == 'aa':
            break
        if '\t' in input_text:
            input_lines.append(tuple(input_text.split('\t')))
        else:
            print("Invalid format. Please use tab to separate album and artist names.")
    return input_lines

def main():
    """Main execution function."""
    try:
        # Get Spotify access token
        access_token = get_spotify_access_token()
        
        # Get input from user
        album_artist_pairs = get_album_input()
        
        if not album_artist_pairs:
            print("No valid input provided.")
            return
            
        # Process each album
        for album_name, artist_name in album_artist_pairs:
            process_album(album_name, artist_name, access_token)
            
        print("\nAll albums processed successfully!")
        
    except Exception as e:
        print(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()