"""CEO-agent: parses the raw idea, delegates to CMO/CTO/CFO, later synthesizes their outputs."""
from venv import logger

from backend.orchestration.state import AgentState
from backend.utils.logger import get_logger
from backend.models.llm_client import call_llm
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