import os
import re
from PIL import ImageFont
from typing import Tuple, List

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename and ensure it's not too long."""
    # Remove invalid characters
    s = re.sub(r'[\/:*?"<>|]', '', filename)
    # Limit length to 255 characters
    return s[:255]

def get_text_dimensions(text_string: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """Calculate the width and height of text with a given font.
    
    Args:
        text_string: The text to measure
        font: The font to use for measurement
        
    Returns:
        tuple: (width, height) of the text
    """
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

def split_text_by_char_limit(text: str, char_limit: int) -> List[str]:
    """Split text into lines based on character limit.
    
    Args:
        text: Text to split
        char_limit: Maximum characters per line
        
    Returns:
        list: Lines of text
    """
    words = text.split()
    lines = []
    current_line = ''
    
    for word in words:
        # If adding the new word exceeds char_limit
        if len(current_line) + len(word) + 1 <= char_limit:
            current_line += (word + ' ')
        else:
            # Add the line if it's not empty
            if current_line:
                lines.append(current_line.strip())
            current_line = word + ' '
            
    # Add the last line
    if current_line:
        lines.append(current_line.strip())
    
    return lines

def fit_text_to_width(text: str, max_width: int, font_path: str, starting_font_size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    """Find the largest font size that fits text within a given width.
    
    Args:
        text: Text to fit
        max_width: Maximum width in pixels
        font_path: Path to the font file
        starting_font_size: Initial font size to try
        index: Font face index for TTC files
        
    Returns:
        ImageFont: Font object with appropriate size
    """
    font_size = starting_font_size
    font = ImageFont.truetype(font_path, font_size, index=index)
    text_width, _ = get_text_dimensions(text, font)
    
    while text_width > max_width and font_size > 0:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size, index=index)
        text_width, _ = get_text_dimensions(text, font)
        
    return font

def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist.
    
    Args:
        directory: Path to directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_save_path(base_dir: str, album_name: str, artist_name: str, suffix: str = "Poster", ext: str = "jpg") -> str:
    """Generate a full save path for a poster.
    
    Args:
        base_dir: Base directory for saving
        album_name: Name of the album
        artist_name: Name of the artist
        suffix: Optional suffix to add to filename
        ext: File extension
        
    Returns:
        str: Full save path
    """
    filename = sanitize_filename(f"{album_name} - {artist_name} {suffix}.{ext}")
    return os.path.join(base_dir, filename)

def calculate_dimensions(image_path: str, target_height: int) -> Tuple[int, int]:
    """Calculate new dimensions maintaining aspect ratio.
    
    Args:
        image_path: Path to the image
        target_height: Desired height in pixels
        
    Returns:
        tuple: (new_width, new_height)
    """
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        new_width = int(target_height * aspect_ratio)
        return (new_width, target_height)