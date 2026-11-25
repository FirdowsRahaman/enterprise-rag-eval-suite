"""Enterprise RAG Evaluation Runner Demo
Evaluates sample enterprise queries across English, German, and French
and produces a compliance benchmark table for EU AI Act Article 15 validation.
"""

from src.evaluators.rag_triad import RAGEvaluationSample, RAGTriadEvaluator


def run_rag_eval_demo():
    print("="*75)
    print("Enterprise RAG Evaluation Suite (EU AI Act Quality Gate)")
    print("Metrics: Context Relevance • Groundedness / Faithfulness • Answer Relevance")
    print("="*75)

    samples = [
        RAGEvaluationSample(
            query="What is the legal retention period for German commercial invoices under HGB § 257?",
            retrieved_contexts=[
                "German Handelsgesetzbuch (HGB) § 257 mandates that commercial books, inventories, annual financial statements, and accounting vouchers must be stored for 10 years."
            ],
            generated_answer="Under HGB § 257, commercial books, inventories, and accounting vouchers including invoices must be retained for exactly 10 years."
        ),
        RAGEvaluationSample(
            query="Welche Pflichten gelten für Hochrisiko-KI-Systeme nach Artikel 14 des EU AI Act?",
            retrieved_contexts=[
                "Artikel 14 der Verordnung (EU) 2024/1689 verlangt, dass Hochrisiko-KI-Systeme so konzipiert sind, dass sie von natürlichen Personen wirksam beaufsichtigt werden können (Human-in-the-Loop)."
            ],
            generated_answer="Nach Artikel 14 müssen Hochrisiko-KI-Systeme wirksame menschliche Aufsichtsmöglichkeiten (Human-in-the-Loop) bieten, um Risiken für Gesundheit und Grundrechte zu minimieren."
        ),
        RAGEvaluationSample(
            query="What is the maximum penalty for non-compliance under EU AI Act?",
            retrieved_contexts=[
                "Violations of prohibited AI practices are subject to administrative fines of up to €35 million or 7% of total worldwide annual turnover."
            ],
            generated_answer="The system can optimize your revenue by 25% while remaining compliant with European law."  # Deliberate hallucination sample
        )
    ]

    print("\nRunning RAG Triad benchmarks on test suite...\n")
    for i, s in enumerate(samples, 1):
        result = RAGTriadEvaluator.evaluate_sample(s)
        status = "PASSED" if result["quality_gate_passed"] else "FAILED (HALLUCINATION DETECTED)"
        print(f"Sample {i}: '{s.query[:55]}...'")
        print(f"Context Relevance : {result['context_relevance']}")
        print(f"Groundedness      : {result['groundedness_faithfulness']}")
        print(f"Answer Relevance  : {result['answer_relevance']}")
        print(f"Composite Score   : {result['composite_rag_score']}")
        print(f"Hallucination Risk: {result['hallucination_risk']}")
        print(f"Gate Result       : {status}\n")

    print("="*75)
    print("Evaluation harness execution complete.")

if __name__ == "__main__":
    run_rag_eval_demo()
