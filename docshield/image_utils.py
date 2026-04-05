"""Image preprocessing utilities."""
import base64
import io
from PIL import Image
from config import MAX_IMAGE_SIZE


def preprocess_image(file_bytes):
    """Resize and convert image to base64 JPEG for Ollama vision."""
    img = Image.open(io.BytesIO(file_bytes))
    img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE))
    if img.mode != "RGB":
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode()
