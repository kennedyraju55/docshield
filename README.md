<div align="center">

![DocShield Banner](https://img.shields.io/badge/DocShield-Medical%20Document%20Security-1f6feb?style=for-the-badge&logo=shield&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com)
[![Gemma 4](https://img.shields.io/badge/Powered%20by-Gemma%204-8B5CF6?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma)

**AI-Powered Medical Document Analysis with Zero Data Leaks**

[Why DocShield](#why-docshield) • [Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Author](#author)

</div>

---

## Why DocShield?

**The Problem:** Millions of patients upload their most sensitive medical data (prescriptions, lab results, hospital bills) to cloud AI services, trading privacy for understanding.

**DocShield's Solution:** Complete AI-powered medical document analysis that runs 100% locally through Gemma 4. Your data never leaves your device.

### Key Impact

- 🛡️ **Zero data transmission** — Processing happens entirely on your machine
- 💊 **Drug interaction detection** — 40+ verified interactions prevent harmful combinations
- 📊 **Lab result explanations** — Medical jargon translated to plain language  
- 💰 **Hospital bill auditing** — Identify overcharges and billing errors
- 🧠 **Gemma 4 showcase** — Multimodal vision, function calling, multi-agent orchestration

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multimodal Vision** | Upload photos or scans of medical documents |
| **Drug Interaction Checking** | Identifies dangerous drug combinations in prescriptions |
| **Lab Result Translation** | Explains blood work, urinalysis, and imaging results in plain language |
| **Hospital Bill Analysis** | Compares charges against national averages to find overcharges |
| **5-Agent Pipeline** | Orchestrator → Reader → Explainer → Checker → Bill Analyzer |
| **Privacy-First** | 100% local processing, works completely offline |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Ollama installed ([ollama.com](https://ollama.com/download))
- Gemma 4 model pulled: `ollama pull gemma4`

### Installation

```bash
git clone https://github.com/kennedyraju55/docshield.git
cd docshield
pip install -r requirements.txt
```

### Docker Quick Start

```bash
docker-compose up
# Web UI at http://localhost:5000
```

### Run Locally

```bash
# Start Gemma 4
ollama serve

# In another terminal
python app.py
# Open http://localhost:5000
```

---

## 🏗️ Architecture

```
User uploads document (photo, scan, text)
          ↓
    +─────────────+
    │ Orchestrator│ ← Classifies: prescription, lab_report, or hospital_bill
    +─────────────+
          ↓
    +─────────────+
    │ Reader      │ ← Gemma 4 Vision: Extracts text from images
    +─────────────+
          ↓
    ┌─────┬─────┬─────┐
    ↓     ↓     ↓     
  Explainer Checker Bill Analyzer
  (Plain   (Drug   (Overcharge
   Lang)   Interactions) Detection)
```

### How It Works

1. **Reader Agent** uses Gemma 4's multimodal vision to extract text from document images
2. **Explainer Agent** translates medical abbreviations and test results to plain language
3. **Checker Agent** uses function calling to query drug interaction database
4. **Bill Analyzer** identifies overcharges by comparing codes against CPT databases
5. **Orchestrator** routes documents to the correct specialist pipeline

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Flask, HTML5, CSS3 |
| **AI/ML** | Gemma 4 (via Ollama), Function Calling |
| **Backend** | Python 3.12, FastAPI |
| **Databases** | Drug interactions (40+), Billing reference (50+ CPT codes) |
| **Deployment** | Docker, Docker Compose |
| **Testing** | pytest (22 tests, all passing) |

---

## 📝 Project Structure

```
docshield/
├── agents/
│   ├── orchestrator.py         Classifies document type
│   ├── reader_agent.py         Gemma 4 Vision: image → text
│   ├── explainer_agent.py      Medical jargon → plain language
│   ├── checker_agent.py        Drug interaction checking
│   └── bill_analyzer_agent.py  Bill auditing
├── tools/
│   ├── drug_interactions.py    40+ drug-drug interactions
│   ├── billing_reference.py    50+ CPT codes with pricing
│   └── tool_registry.py        Function calling setup
├── data/
│   ├── drug_interactions.json
│   ├── billing_codes.json
│   └── medical_abbreviations.json
├── app.py                      Flask web server
├── requirements.txt
└── tests/                      22 unit + integration tests
```

---

## 💻 Demo Use Cases

### ✅ Use Case 1: Prescription Safety Check
Input: A prescription with Warfarin + Ibuprofen  
**DocShield finds:** HIGH RISK interaction causing increased bleeding  
**Result:** Patient avoids dangerous drug combo

### ✅ Use Case 2: Lab Results Explained
Input: Blood glucose (126 mg/dL), HbA1c (6.8%)  
**DocShield explains:** "You're in the pre-diabetic range — talk to your doctor about lifestyle changes"  
**Result:** Patient understands their health status

### ✅ Use Case 3: Hospital Bill Audit
Input: Bill with $8,500 room charge, $950 chest X-ray  
**DocShield flags:** "These charges are 2-3x typical — request itemized bill review"  
**Result:** Patient potentially saves thousands in overcharges

---

## 🧪 Testing

```bash
pytest tests/ -v
# Output: 22 tests PASSING
```

---

## 🔐 Privacy & Security

- ✅ **Zero cloud calls** — No data leaves your device
- ✅ **Offline capable** — Works without internet
- ✅ **No server storage** — Data processed in RAM only
- ✅ **Open source** — Audit the code yourself
- ✅ **HIPAA safe** — No transmission = no violation risk

---

## 👤 Author

**Nrk Raju Guthikonda**  
Senior Software Engineer @ Microsoft  
Copilot Search Infrastructure (Semantic Indexing, RAG)

- 🔗 GitHub: [@kennedyraju55](https://github.com/kennedyraju55)
- ✍️ Dev.to: [nrk-raju-guthikonda](https://dev.to/nrk_raju)
- 💼 LinkedIn: [nrk-raju-guthikonda](https://www.linkedin.com/in/nrk-raju-guthikonda-504066a8/)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<div align="center">

**DocShield** — *Because understanding your health shouldn't require a medical degree.*

Built with Gemma 4 for the Gemma 4 Good Hackathon

</div>
