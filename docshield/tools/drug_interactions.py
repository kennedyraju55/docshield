"""Drug interaction lookup tool."""
import json
import os


class DrugInteractionDB:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "drug_interactions.json")
        with open(os.path.abspath(path)) as f:
            data = json.load(f)
        self.interactions = data["interactions"]
        self.aliases = {k.lower(): v.lower() for k, v in data["aliases"].items()}

    def _normalize(self, drug_name):
        """Normalize drug name: lowercase, resolve brand→generic aliases."""
        name = drug_name.strip().lower()
        return self.aliases.get(name, name)

    def check_interaction(self, drug_a, drug_b):
        """Check if two drugs have a known interaction.
        Returns dict with interaction details or None."""
        a = self._normalize(drug_a)
        b = self._normalize(drug_b)

        if a == b:
            return {"drug_a": drug_a, "drug_b": drug_b, "found": False,
                    "message": "Same drug — no interaction to check."}

        for ix in self.interactions:
            pair = {ix["drug_a"].lower(), ix["drug_b"].lower()}
            if a in pair and b in pair:
                return {
                    "drug_a": drug_a,
                    "drug_b": drug_b,
                    "severity": ix["severity"],
                    "effect": ix["effect"],
                    "recommendation": ix["recommendation"],
                    "found": True,
                }

        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "found": False,
            "message": "No known interaction found in our database. This does not guarantee safety - consult a pharmacist.",
        }

    def check_all_pairs(self, drug_list):
        """Check all pairs in a list of drugs. Returns list of found interactions."""
        results = []
        normalized_list = [(d, self._normalize(d)) for d in drug_list]
        seen = set()

        for i, (name_a, norm_a) in enumerate(normalized_list):
            for j, (name_b, norm_b) in enumerate(normalized_list):
                if i >= j:
                    continue
                pair_key = tuple(sorted([norm_a, norm_b]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                result = self.check_interaction(name_a, name_b)
                if result.get("found"):
                    results.append(result)

        return results


# Singleton instance
_db = None

def get_db():
    global _db
    if _db is None:
        _db = DrugInteractionDB()
    return _db

def check_drug_interaction(drug_a, drug_b):
    """Function callable by LLM tool use."""
    return get_db().check_interaction(drug_a, drug_b)
