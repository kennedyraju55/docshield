"""Orchestrator — classifies document type and routes to the correct agent chain."""
from .base_agent import BaseAgent
from .reader_agent import ReaderAgent
from .explainer_agent import ExplainerAgent
from .checker_agent import CheckerAgent
from .bill_analyzer_agent import BillAnalyzerAgent

CLASSIFY_SYSTEM = """Classify this medical document into exactly ONE of these categories:
- prescription (medication orders, Rx, drug names with dosages)
- lab_report (blood tests, urine tests, pathology, any test results with values)
- hospital_bill (charges, amounts, CPT codes, billing statements, invoices)
- general_medical (other medical documents, visit summaries, referral letters)

Reply with ONLY the category name, nothing else."""


class Orchestrator(BaseAgent):
    def __init__(self, backend):
        super().__init__(backend, "orchestrator")
        self.reader = ReaderAgent(backend)
        self.explainer = ExplainerAgent(backend)
        self.checker = CheckerAgent(backend)
        self.bill_analyzer = BillAnalyzerAgent(backend)

    def _classify(self, text):
        """Classify document type from extracted text."""
        response = self.backend.chat(
            [{"role": "user", "content": f"Classify this document:\n\n{text[:2000]}"}],
            system=CLASSIFY_SYSTEM,
        )
        category = response.get("message", {}).get("content", "").strip().lower()
        valid = {"prescription", "lab_report", "hospital_bill", "general_medical"}
        return category if category in valid else "general_medical"

    def run(self, context):
        """Full pipeline: read → classify → route to specialist agents."""
        # Step 1: Extract text from image (or use provided text)
        yield {"agent": self.name, "header": "Step 1: Reading Document"}
        extracted_text = ""
        for event in self.reader.run(context):
            if event.get("done"):
                extracted_text = event.get("result", "")
            else:
                yield event

        if not extracted_text:
            yield {"agent": self.name, "token": "Could not extract text from the document."}
            yield {"agent": self.name, "done": True, "result": ""}
            return

        # Step 2: Classify document type
        yield {"agent": self.name, "header": "Step 2: Identifying Document Type"}
        doc_type = self._classify(extracted_text)
        yield {"agent": self.name, "doc_type": doc_type,
               "token": f"\nDocument type: **{doc_type.replace('_', ' ').title()}**\n\n"}

        # Build context for downstream agents
        agent_context = {"extracted_text": extracted_text}

        # Step 3: Route to specialist agents
        if doc_type == "prescription":
            yield {"agent": self.name, "header": "Step 3: Explaining Prescription"}
            yield from self.explainer.run(agent_context)
            yield {"agent": self.name, "header": "Step 4: Checking Drug Interactions"}
            yield from self.checker.run(agent_context)

        elif doc_type == "lab_report":
            yield {"agent": self.name, "header": "Step 3: Explaining Lab Results"}
            yield from self.explainer.run(agent_context)

        elif doc_type == "hospital_bill":
            yield {"agent": self.name, "header": "Step 3: Analyzing Bill"}
            yield from self.bill_analyzer.run(agent_context)

        else:  # general_medical
            yield {"agent": self.name, "header": "Step 3: Explaining Document"}
            yield from self.explainer.run(agent_context)
