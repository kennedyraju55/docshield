"""Bill Analyzer Agent — Detects overcharges in hospital bills using function calling."""
import json
from .base_agent import BaseAgent
from ..tools.tool_registry import TOOL_DEFINITIONS, execute_tool_call

BILL_SYSTEM = """You are a medical billing expert helping patients understand their hospital bills and find potential overcharges.

You have access to a billing database via the lookup_procedure_cost tool.

Steps:
1. Extract every line item, charge, and code from the bill
2. For each item, call lookup_procedure_cost to check if the charge is within normal range
3. Flag any item that seems significantly above the typical range
4. Identify duplicate charges (same service billed twice)

Format your final response as:

## Bill Summary
(total charges, number of line items)

## Line-by-Line Review
(for each item: what it is, what you were charged, what's typical, and if it seems fair)

## Potential Issues Found
(overcharges, duplicates, vague codes)

## What To Do
(specific steps to dispute or ask about flagged items)

Be factual. Say "this appears higher than typical" not "you were scammed"."""

BILL_TOOLS = [t for t in TOOL_DEFINITIONS if t["function"]["name"] == "lookup_procedure_cost"]


class BillAnalyzerAgent(BaseAgent):
    def __init__(self, backend):
        super().__init__(backend, "bill_analyzer")

    def run(self, context):
        """Analyze hospital bill for overcharges."""
        extracted_text = context.get("extracted_text", "")
        if not extracted_text:
            yield {"agent": self.name, "token": "No bill text to analyze."}
            yield {"agent": self.name, "done": True, "result": ""}
            return

        yield {"agent": self.name, "header": "Analyzing Your Bill..."}

        messages = [
            {"role": "user", "content": f"Analyze this hospital bill for overcharges and errors:\n\n{extracted_text}"}
        ]

        max_rounds = 10
        for _ in range(max_rounds):
            response = self.backend.chat(messages, system=BILL_SYSTEM, tools=BILL_TOOLS)
            msg = response.get("message", {})
            tool_calls = msg.get("tool_calls")

            if not tool_calls:
                break

            messages.append({"role": "assistant", "content": "", "tool_calls": tool_calls})
            for tc in tool_calls:
                fn_name = tc["function"]["name"]
                fn_args = tc["function"]["arguments"]
                query = fn_args.get("query", "?")
                yield {"agent": self.name, "token": f"\n> Looking up: {query}...\n"}

                result = execute_tool_call(fn_name, fn_args)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })

        final_content = msg.get("content", "")
        if final_content:
            yield {"agent": self.name, "token": final_content}
            yield {"agent": self.name, "done": True, "result": final_content}
        else:
            messages.append({"role": "user", "content": "Now provide your complete bill analysis with all findings."})
            full_text = []
            for token in self.backend.stream_chat(messages, system=BILL_SYSTEM):
                full_text.append(token)
                yield {"agent": self.name, "token": token}
            result = "".join(full_text)
            yield {"agent": self.name, "done": True, "result": result}
