"""CEO-agent: parses the raw idea, delegates to CMO/CTO/CFO, later synthesizes their outputs."""
from backend.orchestration.state import AgentState


def parse_idea(state: AgentState) -> dict:
    idea = state.get("idea", "").strip()
    if not idea:
        return {"errors": state.get("errors", []) + ["No idea provided"], "status": "failed"}
    return {"idea": idea, "status": "running"}


def synthesize(state: AgentState) -> dict:
    cmo = state.get("cmo_output") or {}
    cto = state.get("cto_output") or {}
    cfo = state.get("cfo_output") or {}

    narrative = (
        f"Startup idea: {state.get('idea')}\n"
        f"Market: {cmo.get('tam', 'TBD')}\n"
        f"MVP: {cto.get('mvp_features', 'TBD')}\n"
        f"Funding ask: {cfo.get('funding_ask', 'TBD')}"
    )
    return {"ceo_narrative": narrative}