"""Explainer Agent — Translates medical jargon into plain, simple language."""
import json
import os
from .base_agent import BaseAgent

EXPLAINER_SYSTEM = """You are a friendly medical document explainer. Your job is to take medical text and explain it so that anyone — even someone with no medical background — can understand.

Rules:
- Use simple, everyday language
- Explain what each test result or finding means for the person's health
- If a value is abnormal, explain what that could mean and if they should be concerned
- Explain medical abbreviations when you first use them
- Use bullet points for clarity
- End with a simple "What to do next" recommendation
- Be reassuring but honest — don't downplay serious findings
- NEVER give a diagnosis — say "talk to your doctor about..."

Format:
## What This Document Says
(plain language summary)

## Key Findings
(bullet points of important items)

## What To Do Next
(simple action items)"""


class ExplainerAgent(BaseAgent):
    def __init__(self, backend):
        super().__init__(backend, "explainer")
        self.abbreviations = self._load_abbreviations()

    def _load_abbreviations(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "medical_abbreviations.json")
        try:
            with open(os.path.abspath(path)) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def run(self, context):
        """Explain medical document text in simple language."""
        extracted_text = context.get("extracted_text", "")
        if not extracted_text:
            yield {"agent": self.name, "token": "No text to explain."}
            yield {"agent": self.name, "done": True, "result": ""}
            return

        # Build context with abbreviation hints
        abbrev_hint = ""
        found = [f"{k} = {v}" for k, v in self.abbreviations.items()
                 if k in extracted_text]
        if found:
            abbrev_hint = "\n\nAbbreviations found in document:\n" + "\n".join(found)

        messages = [
            {"role": "user", "content": f"Explain this medical document in simple language:\n\n{extracted_text}{abbrev_hint}"}
        ]

        full_text = []
        yield {"agent": self.name, "header": "Explaining in Simple Language..."}
        for token in self.backend.stream_chat(messages, system=EXPLAINER_SYSTEM):
            full_text.append(token)
            yield {"agent": self.name, "token": token}

        result = "".join(full_text)
        yield {"agent": self.name, "done": True, "result": result}
