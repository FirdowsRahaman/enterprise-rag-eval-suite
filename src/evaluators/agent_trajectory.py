"""Agent Tool-Call Trajectory Evaluator & OpenTelemetry Span Exporter.

Evaluates multi-step agent execution traces along four production axes:
1. Tool Sequence Alignment (ordered LCS match against expected tool trajectory)
2. Tool Precision & Recall (detects redundant, missing, or hallucinated tool calls)
3. Policy & Guardrail Compliance (flags forbidden tools and unrecovered errors)
4. Latency Budget & OTel GenAI Semantic Convention attributes
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCallStep(BaseModel):
    """Single tool invocation observed in an agent execution trace."""

    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    output_summary: str = ""
    latency_ms: float = 0.0
    status: Literal["ok", "error", "blocked"] = "ok"


class TrajectoryEvaluationSample(BaseModel):
    """Expected vs. actual tool-call trajectory for an agentic task."""

    task_id: str
    goal: str
    expected_tool_sequence: list[str]
    actual_steps: list[ToolCallStep]
    forbidden_tools: list[str] = Field(default_factory=list)
    max_total_latency_ms: float = 5000.0


def _lcs_length(expected: list[str], actual: list[str]) -> int:
    """Compute Longest Common Subsequence length for ordered tool alignment."""
    m, n = len(expected), len(actual)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if expected[i - 1] == actual[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


class AgentTrajectoryEvaluator:
    """Evaluates agent tool-call trajectories and emits OTel-compatible span attributes."""

    @staticmethod
    def evaluate_sample(sample: TrajectoryEvaluationSample) -> dict[str, Any]:
        actual_tools = [step.tool_name for step in sample.actual_steps]
        expected_tools = sample.expected_tool_sequence

        # 1. Ordered sequence alignment via LCS
        lcs_len = _lcs_length(expected_tools, actual_tools)
        sequence_alignment = lcs_len / max(1, len(expected_tools))

        # 2. Tool precision & recall
        expected_set = set(expected_tools)
        actual_set = set(actual_tools)
        true_positives = len(expected_set & actual_set)
        tool_precision = true_positives / max(1, len(actual_set))
        tool_recall = true_positives / max(1, len(expected_set))

        # 3. Policy & error compliance
        forbidden_hits = [t for t in actual_tools if t in set(sample.forbidden_tools)]
        error_steps = [s.tool_name for s in sample.actual_steps if s.status != "ok"]
        policy_compliant = len(forbidden_hits) == 0 and len(error_steps) == 0

        # 4. Latency budget
        total_latency_ms = round(sum(s.latency_ms for s in sample.actual_steps), 2)
        within_latency_budget = total_latency_ms <= sample.max_total_latency_ms

        composite_score = round(
            (sequence_alignment * 0.45) + (tool_precision * 0.25) + (tool_recall * 0.30),
            3,
        )
        passed = policy_compliant and within_latency_budget and composite_score >= 0.75

        otel_attributes = {
            "gen_ai.agent.task_id": sample.task_id,
            "gen_ai.agent.tool_calls_count": len(actual_tools),
            "gen_ai.agent.trajectory_score": composite_score,
            "gen_ai.agent.policy_compliant": policy_compliant,
            "gen_ai.agent.total_latency_ms": total_latency_ms,
        }

        return {
            "task_id": sample.task_id,
            "sequence_alignment": round(sequence_alignment, 3),
            "tool_precision": round(tool_precision, 3),
            "tool_recall": round(tool_recall, 3),
            "composite_trajectory_score": composite_score,
            "policy_compliant": policy_compliant,
            "forbidden_tools_called": forbidden_hits,
            "total_latency_ms": total_latency_ms,
            "within_latency_budget": within_latency_budget,
            "quality_gate_passed": passed,
            "otel_attributes": otel_attributes,
        }
