"""Shared state schema passed between all agents in the LangGraph pipeline."""
from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict, total=False):
    # input
    idea: str                          # raw 1-line startup idea from user

    # CMO-agent output (Faiza)
    cmo_output: Optional[Dict[str, Any]]   # {tam, sam, som, competitors, persona, gtm_strategy}

    # CTO-agent output (Lakshit)
    cto_output: Optional[Dict[str, Any]]   # {tech_stack, mvp_features, landing_page_url, code_repo}

    # CFO-agent output (Sakshi)
    cfo_output: Optional[Dict[str, Any]]   # {cost_projection, revenue_model, unit_economics, funding_ask}

    # CEO-agent synthesis (Yeshita)
    ceo_narrative: Optional[str]
    pitch_deck_path: Optional[str]

    # Investor-agent (Yeshita)
    investor_questions: Optional[List[str]]
    investor_transcript: Optional[List[Dict[str, str]]]  # [{q, a}, ...]
    investor_score: Optional[int]          # 0-10

    # meta
    errors: Optional[List[str]]
    status: Optional[str]                  # "pending" | "running" | "done" | "failed"