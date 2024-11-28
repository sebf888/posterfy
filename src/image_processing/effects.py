import numpy as np
from PIL import Image, ImageStat
from skimage.util import random_noise
from skimage.transform import resize
from collections import Counter

def add_noise_to_image(image: Image, val: float = 0.036, intensity: float = 0.35) -> Image:
    """Add artistic noise effect to the image."""
    im_arr = np.array(image) / 255.0
    
    if len(im_arr.shape) == 2:
        rows, cols = im_arr.shape
        channels = 1
    else:
        rows, cols, channels = im_arr.shape
    
    noise_layer = np.zeros((rows, cols))
    for scale in [1, 2, 4]:
        scaled_noise = random_noise(
            np.zeros((rows // scale, cols // scale)),
            mode='gaussian',
            var=(val * scale)**2,
            clip=False
        )
        scaled_noise = resize(scaled_noise, (rows, cols), anti_aliasing=True)
        noise_layer += scaled_noise
    
    noise_layer = (noise_layer - noise_layer.min()) / (noise_layer.max() - noise_layer.min())
    
    if channels == 1:
        noisy_img = im_arr + intensity * noise_layer
    else:
        noisy_img = im_arr + intensity * noise_layer[:, :, np.newaxis]
    
    noisy_img = np.clip(noisy_img, 0, 1)
    noisy_img = (255 * noisy_img).astype(np.uint8)
    
    return Image.fromarray(noisy_img)

def get_dominant_colour(image_path: str, resize_to: int = 50, black_threshold: int = 30, white_threshold: int = 225) -> str:
    """Get the dominant color from an image."""
    with Image.open(image_path) as img:
        img = img.resize((resize_to, resize_to))
        colors = img.getdata()
        color_count = Counter(colors)
        most_common_color, _ = color_count.most_common(1)[0]

        if all(value <= black_threshold for value in most_common_color):
            return "is_black"
        elif all(value >= white_threshold for value in most_common_color):
            return "is_white"
        return None

def get_contrasting_text_color(image_path: str) -> str:
    """Determine the best contrasting text color (black or white) for an image."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img = img.resize((100, 100), Image.LANCZOS)
        avg_color = ImageStat.Stat(img).mean[:3]
        luminance = (0.299 * avg_color[0] + 0.587 * avg_color[1] + 0.114 * avg_color[2]) / 255
        return '#fffffc' if luminance < 0.5 else '#202020'