# DocShield - Privacy-First Medical Document Assistant

> Your medical documents, explained simply. Zero data leaves your device.

Built for the **Kaggle Gemma 4 Good Hackathon** ($200K Prize Pool)

---

## The Problem

Billions of people receive medical documents they can't understand. They upload sensitive health data to cloud AI tools, risking their privacy. Meanwhile:

- **Drug interactions** cause 125,000+ deaths/year in the US alone
- **Billing errors** affect ~80% of hospital bills
- **Health literacy** is low even in developed countries

## The Solution

DocShield is a **multi-agent AI system** powered by **Gemma 4** that reads, explains, and checks your medical documents — entirely on your device.

---

## Use Cases

### 1. Prescription Check

```
INPUT: Photo of prescription
  - Warfarin 5mg daily
  - Lisinopril 10mg daily
  - Ibuprofen 400mg as needed

DOCSHIELD OUTPUT:

  [Reader Agent]     Extracted 4 medications
  [Explainer Agent]  "Warfarin is a blood thinner. Lisinopril 
                      controls blood pressure..."
  [Checker Agent]    !!! HIGH RISK: Warfarin + Ibuprofen
                     "Significantly increased bleeding risk.
                      Avoid NSAIDs with warfarin. Use
                      acetaminophen for pain instead."
                     !! MEDIUM: Ibuprofen + Lisinopril
                     "NSAIDs can reduce blood pressure lowering
                      effect and harm kidneys."
```

### 2. Lab Report Explained

```
INPUT: Blood test results
  LDL: 168 mg/dL    [HIGH]
  HbA1c: 6.8%       [HIGH]
  Creatinine: 1.4   [HIGH]

DOCSHIELD OUTPUT:

  [Explainer Agent]  "Your bad cholesterol (LDL) is high at 168.
                      Target is under 100. Your HbA1c of 6.8%
                      means your average blood sugar over 3 months
                      is in the pre-diabetic range. Your kidney
                      function marker is slightly elevated.
                      Talk to your doctor about diet changes."
```

### 3. Hospital Bill Audit

```
INPUT: Itemized hospital bill ($16,050 total)

DOCSHIELD OUTPUT:

  [Bill Analyzer]    Checking each line item...
  
  > Chest X-ray: Charged $950 | Typical: $50-$300
    POTENTIAL OVERCHARGE: $650 above typical max
    
  > EKG: Charged $450 | Typical: $20-$100
    POTENTIAL OVERCHARGE: $350 above typical max
    
  > IV Saline (x3): Charged $2,400 | Typical: $3-$150
    POTENTIAL OVERCHARGE: wholesale cost is $1/bag
    
  > Room (1 night): Charged $8,500 | Typical: $2,500-$4,500
    POTENTIAL OVERCHARGE: $4,000 above typical max
    
  TOTAL POTENTIAL OVERCHARGES: ~$5,000+
  ACTION: Request itemized bill review from billing dept.
```

---

## Architecture

```
User uploads document (image or text)
           |
    [Orchestrator Agent] -- Classifies document type
           |
    [Reader Agent] -- Gemma 4 Vision (OCR + handwriting)
           |
    Auto-routes to specialist agents:
           |
    +------+------+------+
    |             |             |
[Explainer]  [Checker]    [Bill Analyzer]
  Agent       Agent          Agent
    |            |               |
  Plain      Drug DB        Billing DB
  language   (function       (function
  output      calling)        calling)
```

### Agents

| Agent | Role | Gemma 4 Feature |
|-------|------|----------------|
| **Orchestrator** | Classifies document type, routes to specialists | Text classification |
| **Reader** | Extracts text from photos/scans | Multimodal Vision |
| **Explainer** | Translates jargon to plain language | Long context, reasoning |
| **Checker** | Finds dangerous drug interactions | Native Function Calling |
| **Bill Analyzer** | Flags overcharges and billing errors | Native Function Calling |

---

## Quick Start

```bash
# 1. Install Ollama and pull Gemma 4
ollama pull gemma4

# 2. Clone and install
git clone https://github.com/kennedyraju55/docshield.git
cd docshield
pip install flask pillow requests

# 3. Run
python app.py

# 4. Open http://localhost:5000
```

## Testing

```bash
pip install pytest
pytest tests/ -v    # 22 tests
```

---

## Privacy

- **Zero cloud calls** - Everything runs on your machine via Ollama
- **No data collection** - Your documents never leave your device
- **No internet required** - Works fully offline after setup
- **On-device ready** - Designed for Gemma 4 E4B (runs on phones)

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Model | Gemma 4 (via Ollama locally, Google GenAI on Kaggle) |
| Backend | Python, Flask |
| Frontend | Single-page HTML/JS with SSE streaming |
| Drug Database | 40+ interactions, 50+ brand name aliases |
| Billing Database | 50+ CPT codes with typical US price ranges |
| Testing | pytest (22 tests) |

## Project Structure

```
docshield/
  agents/
    orchestrator.py        - Document classifier + agent router
    reader_agent.py        - Image/text extraction via Gemma 4 vision
    explainer_agent.py     - Medical jargon to plain language
    checker_agent.py       - Drug interaction checker (function calling)
    bill_analyzer_agent.py - Billing error detector (function calling)
  tools/
    drug_interactions.py   - Drug interaction database + lookup
    billing_reference.py   - CPT code + billing database + lookup
    tool_registry.py       - Function calling registry for Gemma 4
  ollama_backend.py        - Local Ollama integration
  kaggle_backend.py        - Kaggle/Google GenAI integration
data/
  drug_interactions.json   - 40+ drug-drug interactions with severity levels
  billing_codes.json       - 50+ CPT codes with typical price ranges
  medical_abbreviations.json - 70+ common medical abbreviations
templates/
  index.html               - Web UI with drag-and-drop upload
tests/
  test_tools.py            - Drug + billing database unit tests
  test_agents.py           - Agent logic tests with mock backend
  test_app.py              - Flask endpoint integration tests
notebook.ipynb             - Kaggle submission notebook
```

---

## Hackathon

- **Competition:** [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon)
- **Track:** Health
- **Prize Pool:** $200,000
- **Deadline:** May 18, 2026

### Gemma 4 Features Showcased

| Feature | Usage |
|---------|-------|
| Multimodal Vision | Reads photos of documents, handwritten prescriptions, scanned reports |
| Native Function Calling | Queries drug interaction DB and billing cost DB via tool calls |
| Multi-Agent Architecture | 5 specialized agents orchestrated in a pipeline |
| On-Device (E4B) | Full privacy, works offline on consumer hardware |
| Long Context (256K) | Handles multi-page medical records |

### Impact

| Problem | Scale | DocShield's Role |
|---------|-------|-----------------|
| Health illiteracy | Billions affected globally | Plain language explanations |
| Drug interactions | 125K+ deaths/year (US) | Automated interaction checking |
| Billing errors | 80% of hospital bills | Cost comparison + overcharge detection |
| Privacy risk | Millions upload health data to cloud | 100% local processing |

---

## License

MIT
