"""Tests for drug interaction and billing lookup tools."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from docshield.tools.drug_interactions import check_drug_interaction, DrugInteractionDB
from docshield.tools.billing_reference import lookup_procedure_cost, BillingDB


class TestDrugInteractions:
    def test_known_interaction(self):
        r = check_drug_interaction("warfarin", "aspirin")
        assert r["found"] is True
        assert r["severity"] == "high"

    def test_no_interaction(self):
        r = check_drug_interaction("acetaminophen", "metformin")
        assert r["found"] is False

    def test_brand_name_alias(self):
        r = check_drug_interaction("Coumadin", "Advil")
        assert r["found"] is True
        assert r["severity"] == "high"

    def test_case_insensitive(self):
        r = check_drug_interaction("WARFARIN", "ASPIRIN")
        assert r["found"] is True

    def test_same_drug(self):
        r = check_drug_interaction("aspirin", "aspirin")
        assert r["found"] is False  # No self-interaction

    def test_check_all_pairs(self):
        db = DrugInteractionDB()
        results = db.check_all_pairs(["warfarin", "aspirin", "ibuprofen"])
        assert len(results) >= 2  # warfarin+aspirin and warfarin+ibuprofen

    def test_serotonin_syndrome(self):
        r = check_drug_interaction("fluoxetine", "tramadol")
        assert r["found"] is True
        assert r["severity"] == "high"

    def test_benzo_opioid(self):
        r = check_drug_interaction("Xanax", "oxycodone")
        assert r["found"] is True
        assert r["severity"] == "high"


class TestBillingReference:
    def test_cpt_code_lookup(self):
        r = lookup_procedure_cost("99213")
        assert r["found"] is True
        assert "office visit" in r["description"].lower()
        assert r["typical_range_usd"] == [100, 250]

    def test_keyword_lookup(self):
        r = lookup_procedure_cost("chest x-ray")
        assert r["found"] is True
        assert "matches" in r

    def test_unknown_code(self):
        r = lookup_procedure_cost("XXXXX")
        assert r["found"] is False

    def test_blood_test_keyword(self):
        r = lookup_procedure_cost("blood test")
        assert r["found"] is True
        assert len(r["matches"]) >= 1

    def test_ekg_keyword(self):
        r = lookup_procedure_cost("ekg")
        assert r["found"] is True
