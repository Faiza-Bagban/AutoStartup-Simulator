"""Investor-agent: fires adversarial questions based on idea category, scores the pitch."""
import json
import random
from pathlib import Path
from backend.orchestration.state import AgentState
from backend.tools.idea_classifier import classify_idea

QUESTION_BANK_PATH = Path("data/question_bank.json")


def _load_question_bank() -> dict:
    with open(QUESTION_BANK_PATH, "r") as f:
        return json.load(f)


def select_questions(state: AgentState, n: int = 5) -> dict:
    bank = _load_question_bank()
    idea_category = classify_idea(state.get("idea", ""))

    questions = list(bank.get("general", []))[:2]
    category_qs = bank.get(idea_category, [])
    if category_qs:
        questions.append(random.choice(category_qs))

    for cat in ["market", "product", "financial"]:
        pool = bank.get(cat, [])
        if pool:
            questions.append(random.choice(pool))

    return {"investor_questions": questions[:n], "investor_transcript": [], "idea_category": idea_category}

def score_pitch(state: AgentState) -> AgentState:
    """Stub scorer — replaced with LLM-based scoring in Week 8."""
    transcript = state.get("investor_transcript", [])
    # placeholder: score based on how many questions got a non-empty answer
    answered = sum(1 for t in transcript if t.get("a"))
    total = max(len(state.get("investor_questions", [])), 1)
    state["investor_score"] = round((answered / total) * 10)
    return state