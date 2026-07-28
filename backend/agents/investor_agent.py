"""Investor-agent: fires adversarial questions based on idea category, scores the pitch."""
import json
import random
from pathlib import Path
from backend.orchestration.state import AgentState

QUESTION_BANK_PATH = Path("data/question_bank.json")


def _load_question_bank() -> dict:
    with open(QUESTION_BANK_PATH, "r") as f:
        return json.load(f)


def select_questions(state: AgentState, n: int = 5) -> AgentState:
    """Pick n questions across categories — general always included, rest randomized."""
    bank = _load_question_bank()
    questions = list(bank.get("general", []))[:2]

    other_categories = [k for k in bank.keys() if k != "general"]
    for cat in other_categories:
        pool = bank.get(cat, [])
        if pool:
            questions.append(random.choice(pool))

    state["investor_questions"] = questions[:n]
    state["investor_transcript"] = []
    return state


def score_pitch(state: AgentState) -> AgentState:
    """Stub scorer — replaced with LLM-based scoring in Week 8."""
    transcript = state.get("investor_transcript", [])
    # placeholder: score based on how many questions got a non-empty answer
    answered = sum(1 for t in transcript if t.get("a"))
    total = max(len(state.get("investor_questions", [])), 1)
    state["investor_score"] = round((answered / total) * 10)
    return state