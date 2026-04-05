"""Abstract LLM backend interface."""
from abc import ABC, abstractmethod


class LLMBackend(ABC):
    @abstractmethod
    def stream_chat(self, messages, system=None):
        """Stream chat completion. Yields token strings."""
        pass

    @abstractmethod
    def chat(self, messages, system=None, tools=None):
        """Non-streaming chat. Returns full response dict."""
        pass

    @abstractmethod
    def stream_vision(self, image_b64, prompt):
        """Stream vision response for an image. Yields token strings."""
        pass
