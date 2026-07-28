"""Test the full graph runs end-to-end with stub agents."""
import pytest
from backend.orchestration.graph import build_graph
from unittest.mock import patch


@patch("backend.agents.ceo_agent.call_llm", return_value="Mocked pitch narrative.")
def test_graph_runs_with_valid_idea(mock_llm):
    app = build_graph()
    result = app.invoke({"idea": "AI-powered plant disease detector for farmers"})

    assert result["status"] == "running"
    assert result["cmo_output"] is not None
    assert result["cto_output"] is not None
    assert result["cfo_output"] is not None
    assert result["ceo_narrative"] == "Mocked pitch narrative."
    assert len(result["investor_questions"]) > 0
    assert len(result["investor_transcript"]) == len(result["investor_questions"])
    assert result["investor_score"] is not None


def test_graph_fails_gracefully_on_empty_idea():
    app = build_graph()
    result = app.invoke({"idea": ""})
    assert result["status"] == "failed"
    assert "No idea provided" in result["errors"]


@patch("backend.agents.ceo_agent.call_llm", return_value="Mocked answer.")
def test_investor_score_in_valid_range(mock_llm):
    app = build_graph()
    result = app.invoke({"idea": "Subscription box for eco-friendly cleaning products"})
    assert 0 <= result["investor_score"] <= 10

