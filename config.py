"""DocShield configuration."""
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("DOCSHIELD_MODEL", "gemma4")
VISION_MODEL = os.environ.get("DOCSHIELD_VISION_MODEL", MODEL)

MAX_IMAGE_SIZE = 1024  # Max dimension for image resize
MAX_INPUT_CHARS = 8000
STREAM_TIMEOUT = 600
