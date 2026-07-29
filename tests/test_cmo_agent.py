"""Tests for CMOAgent"""
import pytest
from backend.agents.cmo_agent import CMOAgent


def test_clean_json_strips_fences():
    agent = CMOAgent()
    raw = '```json\n{"key": "value"}\n```'
    result = agent._clean_json(raw)
    assert result == '{"key": "value"}'


def test_clean_json_passthrough_plain():
    agent = CMOAgent()
    raw = '{"key": "value"}'
    result = agent._clean_json(raw)
    assert result == '{"key": "value"}'


def test_analyze_market_returns_dict_keys():
    agent = CMOAgent()
    result = agent.analyze_market("AI-powered note-taking app")
    assert set(["tam", "sam", "som", "reasoning"]).issubset(result.keys())


def test_scan_competitors_returns_list():
    agent = CMOAgent()
    result = agent.scan_competitors("AI-powered note-taking app")
    assert isinstance(result, list)
    assert len(result) > 0


def test_generate_persona_returns_dict_keys():
    agent = CMOAgent()
    result = agent.generate_persona("AI-powered note-taking app")
    assert set(["name", "age_range", "occupation"]).issubset(result.keys())