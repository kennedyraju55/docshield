"""Reader Agent — Extracts text from medical document images using Gemma 4 vision."""
from .base_agent import BaseAgent

READER_PROMPT = """You are a medical document reader. Extract ALL text from this medical document image accurately.

Rules:
- Extract every word, number, date, and code visible in the document
- Preserve the structure (headers, sections, line items)
- If handwriting is unclear, write [unclear] next to your best guess
- Do NOT interpret or explain — just extract the raw text
- Include patient names, dates, medication names, dosages, codes, amounts

Output the extracted text exactly as it appears in the document."""


class ReaderAgent(BaseAgent):
    def __init__(self, backend):
        super().__init__(backend, "reader")

    def run(self, context):
        """Extract text from document image or pass through existing text."""
        image_b64 = context.get("image_b64")
        text = context.get("text")

        # If text already provided, skip vision
        if text and not image_b64:
            yield {"agent": self.name, "token": text}
            yield {"agent": self.name, "done": True, "result": text}
            return

        if not image_b64:
            yield {"agent": self.name, "token": "ERROR: No image provided."}
            yield {"agent": self.name, "done": True, "result": ""}
            return

        full_text = []
        yield {"agent": self.name, "header": "Reading Document..."}
        for token in self.backend.stream_vision(image_b64, READER_PROMPT):
            full_text.append(token)
            yield {"agent": self.name, "token": token}

        result = "".join(full_text)
        yield {"agent": self.name, "done": True, "result": result}
