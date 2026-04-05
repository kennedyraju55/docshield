"""Kaggle backend using Google GenAI SDK for Gemma 4 access."""
import json
from .llm_backend import LLMBackend


class KaggleBackend(LLMBackend):
    """Backend for running on Kaggle with google-generativeai SDK."""

    def __init__(self, model_name="gemma-4-27b-it"):
        try:
            import google.generativeai as genai
            self.genai = genai
            self.model = genai.GenerativeModel(model_name)
        except ImportError:
            raise ImportError("google-generativeai is required. Install with: pip install google-generativeai")

    def stream_chat(self, messages, system=None):
        """Stream chat completion."""
        prompt = self._messages_to_prompt(messages, system)
        response = self.model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def chat(self, messages, system=None, tools=None):
        """Non-streaming chat with optional tool use."""
        prompt = self._messages_to_prompt(messages, system)

        if tools:
            # Convert tool definitions to Gemma format
            gemma_tools = self._convert_tools(tools)
            response = self.model.generate_content(prompt, tools=gemma_tools)
        else:
            response = self.model.generate_content(prompt)

        # Parse response
        result = {"message": {"content": response.text if response.text else ""}}

        # Check for function calls
        if hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    fc = part.function_call
                    result["message"]["tool_calls"] = [{
                        "function": {
                            "name": fc.name,
                            "arguments": dict(fc.args),
                        }
                    }]
                    result["message"]["content"] = ""
                    break

        return result

    def stream_vision(self, image_b64, prompt):
        """Stream vision response."""
        import base64
        from PIL import Image
        import io

        image_bytes = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(image_bytes))

        response = self.model.generate_content([prompt, img], stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def _messages_to_prompt(self, messages, system=None):
        """Convert message list to a single prompt string."""
        parts = []
        if system:
            parts.append(f"System: {system}\n")
        if isinstance(messages, str):
            parts.append(messages)
        else:
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "tool":
                    parts.append(f"Tool result: {content}")
                else:
                    parts.append(content)
        return "\n\n".join(parts)

    def _convert_tools(self, tools):
        """Convert OpenAI-style tool defs to Gemma format."""
        gemma_tools = []
        for t in tools:
            if t.get("type") == "function":
                fn = t["function"]
                gemma_tools.append(self.genai.protos.Tool(
                    function_declarations=[
                        self.genai.protos.FunctionDeclaration(
                            name=fn["name"],
                            description=fn["description"],
                            parameters=fn["parameters"],
                        )
                    ]
                ))
        return gemma_tools
