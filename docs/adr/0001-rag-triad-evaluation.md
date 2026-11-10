# 1. Adopt the RAG Triad for Deterministic Accuracy Verification

Date: 2026-02-05

## Status
Accepted

## Context
Traditional lexical metrics (BLEU, ROUGE) correlate poorly with human judgments of factual correctness and are unable to detect subtle hallucinations in enterprise RAG pipelines.

## Decision
We adopt the **RAG Triad** framework (Context Relevance, Faithfulness, Answer Relevance) as our standard evaluation metric suite.

## Consequences
- Provides mathematical explainability for model outputs.
- Fulfills EU AI Act Article 15 requirements for continuous accuracy benchmarking.
