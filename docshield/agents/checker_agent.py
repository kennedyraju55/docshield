"""Checker Agent — Flags drug interactions using function calling."""
import json
from .base_agent import BaseAgent
from ..tools.tool_registry import TOOL_DEFINITIONS, execute_tool_call

CHECKER_SYSTEM = """You are a medication safety checker. Given a medical document, identify ALL medications mentioned and check for dangerous drug interactions.

You have access to a drug interaction database via the check_drug_interaction tool.

Steps:
1. Extract every medication name from the document
2. For each pair of medications, call check_drug_interaction to check for interactions
3. Summarize your findings clearly

Format your final response as:

## Medications Found
(list all medications)

## Interaction Warnings
(for each interaction found, explain the risk in simple language)

## Safety Summary
(overall assessment and what to discuss with doctor/pharmacist)

If no interactions are found, reassure the user but remind them to always consult their pharmacist."""

# Only include drug interaction tool for the checker
CHECKER_TOOLS = [t for t in TOOL_DEFINITIONS if t["function"]["name"] == "check_drug_interaction"]


class CheckerAgent(BaseAgent):
    def __init__(self, backend):
        super().__init__(backend, "checker")

    def run(self, context):
        """Check for drug interactions in the extracted text."""
        extracted_text = context.get("extracted_text", "")
        if not extracted_text:
            yield {"agent": self.name, "token": "No text to check."}
            yield {"agent": self.name, "done": True, "result": ""}
            return

        yield {"agent": self.name, "header": "Checking Drug Interactions..."}

        messages = [
            {"role": "user", "content": f"Check all drug interactions in this medical document:\n\n{extracted_text}"}
        ]

        # Step 1: Ask LLM to identify drugs and call tools
        max_rounds = 5
        for _ in range(max_rounds):
            response = self.backend.chat(messages, system=CHECKER_SYSTEM, tools=CHECKER_TOOLS)

            msg = response.get("message", {})
            tool_calls = msg.get("tool_calls")

            if not tool_calls:
                # No more tool calls — this is the final response
                break

            # Execute tool calls — append clean assistant message
            messages.append({"role": "assistant", "content": "", "tool_calls": tool_calls})
            for tc in tool_calls:
                fn_name = tc["function"]["name"]
                fn_args = tc["function"]["arguments"]
                yield {"agent": self.name, "token": f"\n> Checking: {fn_args.get('drug_a', '?')} + {fn_args.get('drug_b', '?')}...\n"}

                result = execute_tool_call(fn_name, fn_args)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })

        # Step 2: Stream the final summary
        final_content = msg.get("content", "")
        if final_content:
            # Already have final response from non-streaming call
            yield {"agent": self.name, "token": final_content}
            yield {"agent": self.name, "done": True, "result": final_content}
        else:
            # Stream a final synthesis
            messages.append({"role": "user", "content": "Now summarize all the interaction check results clearly."})
            full_text = []
            for token in self.backend.stream_chat(messages, system=CHECKER_SYSTEM):
                full_text.append(token)
                yield {"agent": self.name, "token": token}
            result = "".join(full_text)
            yield {"agent": self.name, "done": True, "result": result}
