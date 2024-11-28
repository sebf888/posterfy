from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from .effects import add_noise_to_image, get_contrasting_text_color
from ..utils.helpers import get_text_dimensions, split_text_by_char_limit

def create_poster_base(full_path: str) -> Image:
    """Create the base poster from an album cover."""
    album_cover = Image.open(full_path)
    poster_width = 6600
    poster_height = 9600

    scale_factor = poster_height / album_cover.height
    new_width = int(album_cover.width * scale_factor)
    album_cover_resized = album_cover.resize((new_width, poster_height), Image.Resampling.LANCZOS)

    left_margin = (new_width - poster_width) // 2
    right_margin = new_width - left_margin

    return album_cover_resized.crop((left_margin, 0, right_margin, poster_height))

def create_alternate_poster(album_name: str, artist_name: str, description: str, full_path: str) -> Image:
    """Generate an artistic poster with album information."""
    # Font settings
    futura_font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
    char_limit = 12 if len(album_name) <= 20 else (15 if len(album_name) <= 30 else 24)
    
    # Create base poster
    poster_alternate = create_poster_base(full_path)
    poster_width, poster_height = poster_alternate.size
    
    # Calculate dimensions and positions
    max_title_width = poster_width * 0.95
    x_coord = (poster_width - max_title_width) / 2
    y_coord = 770
    
    # Prepare text content
    wrapped_description = textwrap.fill(description, width=154)
    text_colour = get_contrasting_text_color(full_path)
    
    # Initialize drawing
    draw = ImageDraw.Draw(poster_alternate)
    
    # Font sizes
    starting_font_size = 2000
    artist_name_font_size = 180
    xs_font_size = 84
    
    # Draw album name
    album_name_lines = split_text_by_char_limit(album_name.upper(), char_limit)
    album_name_font = ImageFont.truetype(futura_font_path, starting_font_size, index=2)
    
    y_text = y_coord
    for line in album_name_lines:
        width, text_height = get_text_dimensions(line, album_name_font)
        draw.text((3600, y_text), line, font=album_name_font, fill=text_colour, anchor="ma")
        y_text += text_height - (text_height * 0.18)
    
    # Draw artist name
    artist_name_font = ImageFont.truetype(futura_font_path, artist_name_font_size, index=2)
    artist_name_y_coord = y_text + (text_height * 0.23)
    draw.text((3600, artist_name_y_coord), artist_name.upper(), 
              font=artist_name_font, fill=text_colour, anchor="ma")
    
    # Draw description
    xs_font = ImageFont.truetype(futura_font_path, xs_font_size)
    draw.multiline_text(
        (3600, 9150),
        wrapped_description,
        font=xs_font,
        fill=text_colour,
        anchor='mm',
        align='center'
    )
    
    # Add noise effect
    return add_noise_to_image(poster_alternate)