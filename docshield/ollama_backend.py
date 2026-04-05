"""Ollama implementation of LLM backend."""
import json
import requests
from .llm_backend import LLMBackend
from config import OLLAMA_URL, MODEL, VISION_MODEL, STREAM_TIMEOUT


class OllamaBackend(LLMBackend):
    def __init__(self, model=None, vision_model=None):
        self.model = model or MODEL
        self.vision_model = vision_model or VISION_MODEL
        self.chat_url = f"{OLLAMA_URL}/api/chat"
        self.tags_url = f"{OLLAMA_URL}/api/tags"

    def stream_chat(self, messages, system=None):
        """Stream chat completion. Yields token strings."""
        payload = {
            "model": self.model,
            "messages": self._build_messages(messages, system),
            "stream": True,
        }
        try:
            resp = requests.post(self.chat_url, json=payload, stream=True, timeout=STREAM_TIMEOUT)
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done", False):
                        break
        except requests.ConnectionError:
            yield "ERROR: Cannot connect to Ollama. Make sure it is running."
        except Exception as e:
            yield f"ERROR: {e}"

    def chat(self, messages, system=None, tools=None):
        """Non-streaming chat. Returns full response dict."""
        payload = {
            "model": self.model,
            "messages": self._build_messages(messages, system),
            "stream": False,
        }
        if tools:
            payload["tools"] = tools
        resp = requests.post(self.chat_url, json=payload, timeout=STREAM_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def stream_vision(self, image_b64, prompt):
        """Stream vision response for a base64-encoded image."""
        payload = {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_b64],
                }
            ],
            "stream": True,
        }
        try:
            resp = requests.post(self.chat_url, json=payload, stream=True, timeout=STREAM_TIMEOUT)
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done", False):
                        break
        except requests.ConnectionError:
            yield "ERROR: Cannot connect to Ollama. Make sure it is running."
        except Exception as e:
            yield f"ERROR: {e}"

    def health_check(self):
        """Check Ollama connectivity and model availability."""
        try:
            r = requests.get(self.tags_url, timeout=5)
            models = [m["name"] for m in r.json().get("models", [])]
            model_available = any(self.model in m for m in models)
            return {
                "status": "healthy" if model_available else "model_missing",
                "ollama": "connected",
                "models": models,
                "target_model": self.model,
                "model_available": model_available,
            }
        except Exception:
            return {
                "status": "error",
                "ollama": "disconnected",
                "message": "Ollama is not running. Start it with 'ollama serve'",
            }

    def _build_messages(self, messages, system=None):
        """Prepend system message if provided."""
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        if isinstance(messages, str):
            msgs.append({"role": "user", "content": messages})
        else:
            msgs.extend(messages)
        return msgs
