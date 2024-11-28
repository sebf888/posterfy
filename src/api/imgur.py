import base64
import requests
from ..config import IMGUR_CLIENT_ID

def upload_to_imgur(image_path: str) -> str:
    """Upload an image to Imgur and return the URL."""
    headers = {
        "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
    }

    try:
        with open(image_path, 'rb') as image:
            base64_image = base64.b64encode(image.read()).decode('utf-8')
            data = {
                'image': base64_image,
                'type': 'base64'
            }
            response = requests.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                return response.json()['data']['link']
            else:
                raise Exception(f"Imgur upload failed: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error uploading to Imgur: {str(e)}")