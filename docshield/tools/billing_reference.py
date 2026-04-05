"""Billing reference lookup tool."""
import json
import os


class BillingDB:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "billing_codes.json")
        with open(os.path.abspath(path)) as f:
            data = json.load(f)
        self.procedures = data["procedures"]
        self.common_overcharges = data["common_overcharges"]
        self.keywords = data["keywords"]

    def lookup(self, query):
        """Look up procedure cost by CPT code or description keyword."""
        query = query.strip()

        # Direct CPT code lookup
        if query in self.procedures:
            proc = self.procedures[query]
            return {
                "found": True,
                "cpt_code": query,
                "description": proc["description"],
                "typical_range_usd": proc["typical_range"],
                "median_usd": proc["median"],
            }

        # Keyword search
        q_lower = query.lower()
        for keyword, codes in self.keywords.items():
            if keyword in q_lower or q_lower in keyword:
                results = []
                for code in codes:
                    if code in self.procedures:
                        proc = self.procedures[code]
                        results.append({
                            "cpt_code": code,
                            "description": proc["description"],
                            "typical_range_usd": proc["typical_range"],
                            "median_usd": proc["median"],
                        })
                if results:
                    return {"found": True, "matches": results}

        return {
            "found": False,
            "message": f"No billing data found for '{query}'. This doesn't mean the charge is wrong — consult your insurance provider.",
        }


_db = None

def get_db():
    global _db
    if _db is None:
        _db = BillingDB()
    return _db

def lookup_procedure_cost(query):
    """Function callable by LLM tool use."""
    return get_db().lookup(query)
