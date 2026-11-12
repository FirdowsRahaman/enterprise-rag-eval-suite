# Enterprise RAG Evaluation Suite (EU AI Act Quality Gate) 

<p align="left">
  <img src="https://img.shields.io/badge/Evaluation-RAG%20Triad%20%7C%20Faithfulness-10B981?style=flat-square" alt="RAG Triad">
  <a href="EU_AI_ACT_TECHNICAL_DOCUMENTATION.md"><img src="https://img.shields.io/badge/Compliance-EU%20AI%20Act%20Art.%2015-8B5CF6?style=flat-square" alt="EU AI Act"></a>
  <a href="docs/adr/"><img src="https://img.shields.io/badge/Architecture-ADRs-F59E0B?style=flat-square" alt="ADRs"></a>
  <img src="https://img.shields.io/badge/Language-Multilingual%20(DE%20%7C%20FR%20%7C%20EN)-0EA5E9?style=flat-square" alt="Multilingual">
</p>

A production-grade evaluation harness and CI/CD quality gate for Enterprise Retrieval-Augmented Generation (RAG) platforms. Measures **Context Relevance**, **Groundedness / Faithfulness**, and **Answer Relevance** with multilingual support across European languages to satisfy **EU AI Act Article 15 (Accuracy, Robustness & Cybersecurity)** compliance mandates.

---

## Table of Contents
- [The Production RAG Challenge](#the-production-rag-challenge)
- [The RAG Triad Metrics](#the-rag-triad-metrics)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [CI/CD Quality Gate Integration](#cicd-quality-gate-integration)
- [License](#license)

---

## The Production RAG Challenge

In enterprise environments, an un-evaluated RAG pipeline is a liability. Generating inaccurate legal, financial, or medical guidance exposes organizations to severe regulatory liability and loss of customer trust.

This suite provides deterministic, automated evaluation metrics to detect:
1. **Retrieval Failure**: Did the vector database fetch irrelevant chunks?
2. **Hallucination / Ungrounded Claims**: Did the LLM assert facts not present in the retrieved European documentation?
3. **Question Drift**: Did the LLM evade the user's specific prompt?

---

## The RAG Triad Metrics

```
                     [ User Question ]
                            │
               ┌────────────┴────────────┐
               │                         │
     (Context Relevance)          (Answer Relevance)
               │                         │
               ▼                         ▼
      [ Retrieved Context ] ──────▶ [ LLM Answer ]
                      (Faithfulness / Groundedness)
```

1. **Context Relevance**: Evaluates whether retrieved document chunks contain the information necessary to answer the prompt.
2. **Groundedness (Faithfulness)**: Mathematical validation ensuring every claim in the response is traced back to source citations.
3. **Answer Relevance**: Checks whether the final response addresses the original user intent.

---

## Quick Start

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/FirdowsRahaman/enterprise-rag-eval-suite.git
   cd enterprise-rag-eval-suite
   pip install -r requirements.txt
   ```

2. **Run Evaluation Harness Demo**:
   ```bash
   python demo/run_evaluation.py
   ```

---

## License
This project is licensed under the MIT License.
