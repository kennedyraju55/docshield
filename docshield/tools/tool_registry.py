"""Registry mapping function names to callables for LLM function calling."""
import json
from .drug_interactions import check_drug_interaction
from .billing_reference import lookup_procedure_cost


TOOL_FUNCTIONS = {
    "check_drug_interaction": check_drug_interaction,
    "lookup_procedure_cost": lookup_procedure_cost,
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "check_drug_interaction",
            "description": "Check if two medications have a known interaction that could be harmful",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_a": {"type": "string", "description": "First medication name (brand or generic)"},
                    "drug_b": {"type": "string", "description": "Second medication name (brand or generic)"},
                },
                "required": ["drug_a", "drug_b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_procedure_cost",
            "description": "Look up the typical cost range for a medical procedure or service by CPT code or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "CPT code (e.g. '99213') or procedure description (e.g. 'chest x-ray')"},
                },
                "required": ["query"],
            },
        },
    },
]


def execute_tool_call(name, arguments):
    """Execute a tool function by name with given arguments."""
    fn = TOOL_FUNCTIONS.get(name)
    if not fn:
        return {"error": f"Unknown function: {name}"}
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    return fn(**arguments)
