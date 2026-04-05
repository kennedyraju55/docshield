"""Tests for agents using a mock LLM backend."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from docshield.llm_backend import LLMBackend
from docshield.agents.reader_agent import ReaderAgent
from docshield.agents.explainer_agent import ExplainerAgent


class MockBackend(LLMBackend):
    """Mock backend that returns predefined responses."""
    def __init__(self, response="Mock response"):
        self.response = response

    def stream_chat(self, messages, system=None):
        for word in self.response.split():
            yield word + " "

    def chat(self, messages, system=None, tools=None):
        return {"message": {"content": self.response}}

    def stream_vision(self, image_b64, prompt):
        for word in self.response.split():
            yield word + " "


class TestReaderAgent:
    def test_text_passthrough(self):
        """When text is provided, reader should pass it through without vision."""
        backend = MockBackend()
        agent = ReaderAgent(backend)
        events = list(agent.run({"text": "Sample medical text"}))
        result_event = [e for e in events if e.get("done")]
        assert len(result_event) == 1
        assert result_event[0]["result"] == "Sample medical text"

    def test_no_input(self):
        """When no image or text, should return error."""
        backend = MockBackend()
        agent = ReaderAgent(backend)
        events = list(agent.run({}))
        tokens = "".join(e.get("token", "") for e in events)
        assert "ERROR" in tokens or "No image" in tokens

    def test_vision_mode(self):
        """When image is provided, should use vision."""
        backend = MockBackend("Extracted medical text from image")
        agent = ReaderAgent(backend)
        events = list(agent.run({"image_b64": "fakebase64data"}))
        result = [e for e in events if e.get("done")][0]["result"]
        assert "Extracted" in result


class TestExplainerAgent:
    def test_explains_text(self):
        backend = MockBackend("Your blood sugar is high.")
        agent = ExplainerAgent(backend)
        events = list(agent.run({"extracted_text": "HbA1c: 6.8%"}))
        result = [e for e in events if e.get("done")][0]["result"]
        assert "blood sugar" in result.lower() or "high" in result.lower()

    def test_no_text(self):
        backend = MockBackend()
        agent = ExplainerAgent(backend)
        events = list(agent.run({}))
        tokens = "".join(e.get("token", "") for e in events)
        assert "No text" in tokens
