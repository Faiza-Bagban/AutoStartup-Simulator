"""CEO-agent: parses the raw idea, delegates to CMO/CTO/CFO, later synthesizes their outputs."""
from venv import logger

from backend.orchestration.state import AgentState
from backend.utils.logger import get_logger
from backend.models.llm_client import call_llm
from backend.agents.investor_agent import generate_rebuttal
logger = get_logger(__name__)

def parse_idea(state: AgentState) -> dict:
    idea = state.get("idea", "").strip()
    if not idea:
        return {"errors": state.get("errors", []) + ["No idea provided"], "status": "failed"}
    logger.info(f"Idea parsed: {state['idea']}")
    return {"idea": idea, "status": "running"}

def synthesize(state: AgentState) -> dict:
    cmo = state.get("cmo_output") or {}
    cto = state.get("cto_output") or {}
    cfo = state.get("cfo_output") or {}

    prompt = (
        f"Idea: {state.get('idea')}\n"
        f"Market research: {cmo}\n"
        f"Tech/MVP: {cto}\n"
        f"Financials: {cfo}\n\n"
        "Write a tight 4-6 sentence startup pitch narrative combining all of this. "
        "Sound confident, specific, investor-ready. No fluff."
    )
    narrative = call_llm(prompt, system="You are a sharp startup CEO writing your own pitch narrative.")
    return {"ceo_narrative": narrative or "Narrative generation failed — check GROQ_API_KEY."}

def defend_rebuttal(question: str, original_answer: str, rebuttal: str, narrative: str) -> str:
    """CEO responds to investor's pushback — second round."""
    prompt = (
        f"Startup narrative: {narrative}\n"
        f"Original question: {question}\n"
        f"Your first answer: {original_answer}\n"
        f"Investor's pushback: {rebuttal}\n\n"
        "Defend your position with more specifics — 2-3 sentences. Don't just repeat yourself."
    )
    from backend.models.llm_client import call_llm
    return call_llm(prompt, system="You are the CEO, holding your ground under investor scrutiny.").strip()

def answer_investor_questions(state: AgentState) -> dict:
    from backend.agents.investor_agent import generate_rebuttal

    questions = state.get("investor_questions", [])
    narrative = state.get("ceo_narrative", "")
    transcript = []

    for q in questions:
        prompt = (
            f"Startup narrative: {narrative}\n\n"
            f"Investor question: {q}\n\n"
            "Answer as the CEO — confident, specific, 2-3 sentences max."
        )
        answer = call_llm(prompt, system="You are the CEO defending your startup pitch to a skeptical investor.")

        rebuttal = generate_rebuttal(q, answer)
        entry = {"q": q, "a": answer or "No answer generated."}

        if rebuttal and rebuttal != "NO_REBUTTAL":
            defense = defend_rebuttal(q, answer, rebuttal, narrative)
            entry["rebuttal"] = rebuttal
            entry["defense"] = defense

        transcript.append(entry)

    return {"investor_transcript": transcript}