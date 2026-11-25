"""Unit tests for RAG Triad and Agent Tool-Call Trajectory evaluators."""

from src.evaluators.agent_trajectory import (
    AgentTrajectoryEvaluator,
    ToolCallStep,
    TrajectoryEvaluationSample,
)
from src.evaluators.rag_triad import RAGEvaluationSample, RAGTriadEvaluator


def test_rag_triad_passes_grounded_answer():
    sample = RAGEvaluationSample(
        query="German commercial books accounting vouchers retention period",
        retrieved_contexts=[
            "German commercial books inventories annual financial statements accounting vouchers retained years."
        ],
        generated_answer="German commercial books accounting vouchers retained years.",
    )
    res = RAGTriadEvaluator.evaluate_sample(sample)
    assert res["quality_gate_passed"] is True
    assert res["hallucination_risk"] == "Low"


def test_rag_triad_flags_hallucination():
    sample = RAGEvaluationSample(
        query="What is the maximum penalty under EU AI Act?",
        retrieved_contexts=["Prohibited AI practices carry fines up to 35 million EUR."],
        generated_answer="Your quarterly revenue will grow by 25% automatically.",
    )
    res = RAGTriadEvaluator.evaluate_sample(sample)
    assert res["quality_gate_passed"] is False
    assert res["hallucination_risk"] == "High"


def test_agent_trajectory_passes_optimal_trace():
    sample = TrajectoryEvaluationSample(
        task_id="sql-compliance-01",
        goal="Query EU customer revenue with RBAC check",
        expected_tool_sequence=["validate_rbac", "ast_sql_guard", "execute_duckdb"],
        actual_steps=[
            ToolCallStep(tool_name="validate_rbac", latency_ms=12.5, status="ok"),
            ToolCallStep(tool_name="ast_sql_guard", latency_ms=8.2, status="ok"),
            ToolCallStep(tool_name="execute_duckdb", latency_ms=45.0, status="ok"),
        ],
        forbidden_tools=["drop_table", "raw_shell"],
    )
    res = AgentTrajectoryEvaluator.evaluate_sample(sample)
    assert res["quality_gate_passed"] is True
    assert res["composite_trajectory_score"] == 1.0
    assert res["otel_attributes"]["gen_ai.agent.policy_compliant"] is True


def test_agent_trajectory_blocks_forbidden_tool():
    sample = TrajectoryEvaluationSample(
        task_id="sql-compliance-02",
        goal="Query EU customer revenue with RBAC check",
        expected_tool_sequence=["validate_rbac", "ast_sql_guard", "execute_duckdb"],
        actual_steps=[
            ToolCallStep(tool_name="validate_rbac", latency_ms=10.0, status="ok"),
            ToolCallStep(tool_name="raw_shell", latency_ms=30.0, status="blocked"),
        ],
        forbidden_tools=["raw_shell"],
    )
    res = AgentTrajectoryEvaluator.evaluate_sample(sample)
    assert res["quality_gate_passed"] is False
    assert res["policy_compliant"] is False
    assert res["forbidden_tools_called"] == ["raw_shell"]
