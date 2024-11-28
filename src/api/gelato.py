import json
import requests
from ..config import GELATO_API_KEY, GELATO_STORE_ID

def upload_to_gelato(poster_public_url: str, album_name: str, artist_name: str) -> dict:
    """Create a product listing on Gelato."""
    headers = {
        'X-API-KEY': GELATO_API_KEY,
        'Content-Type': 'application/json'
    }

    album_name = album_name.title()
    artist_name = artist_name.title()

    data = {
        "templateId": "1eafe09e-603c-4f29-8bcf-2e33f843c56a",
        "title": f"{album_name} - {artist_name} | Wall Art Decor | Music Rap Album Poster | Print ",
        "description": f"""{album_name} by {artist_name} Poster - Exclusively Designed by the Blue Dove team in 2023.
        
        Why Choose Blue Dove Posters?
        
        🎨 Unparalleled Artistry: Our commitment is to deliver exceptional artworks that elevate any space.
        🌿 Eco-Friendly Materials: Museum-quality paper (220gsm semi-glossy) from FSC certified forests.
        🌍 Global Yet Local: Worldwide production network for quick delivery and reduced emissions.
        🖼️ Framed to Perfection: Sustainably sourced pine frames with shatterproof plexiglass.
        """,
        "isVisibleInTheOnlineStore": False,
        "salesChannels": ["web"],
        "tags": [artist_name, album_name, "luxury", "prints", "decor", "rap", "music"],
        "variants": [
            {
                "templateVariantId": variant_id,
                "imagePlaceholders": [
                    {
                        "name": "BG Image Layer 1",
                        "fileUrl": poster_public_url
                    }
                ]
            }
            for variant_id in [
                "7dfb391e-1a30-47f6-b78b-788c948045b0",
                "5a332bb0-4905-4832-b3f1-a3eb987f4526",
                "73d05537-9fba-438f-8c37-1d0984b034e5",
                "70bc9274-ffa2-4194-8c6d-548dbe29866a"
            ]
        ]
    }

    response = requests.post(
        f"https://ecommerce.gelatoapis.com/v1/stores/{GELATO_STORE_ID}/products:create-from-template",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code != 200:
        raise Exception(f"Gelato API Error: {response.status_code}")
    
    return response.json()