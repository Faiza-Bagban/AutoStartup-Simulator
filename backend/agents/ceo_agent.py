"""CEO-agent: parses the raw idea, delegates to CMO/CTO/CFO, later synthesizes their outputs."""
from backend.orchestration.state import AgentState


def parse_idea(state: AgentState) -> AgentState:
    """Entry node — validate/clean the idea, set status."""
    idea = state.get("idea", "").strip()
    if not idea:
        state["errors"] = state.get("errors", []) + ["No idea provided"]
        state["status"] = "failed"
        return state

    state["idea"] = idea
    state["status"] = "running"
    return state


def synthesize(state: AgentState) -> AgentState:
    """Runs AFTER CMO/CTO/CFO nodes complete — combines their outputs into one narrative.
    Stubbed for now; full LLM-based synthesis wired in Week 3."""
    cmo = state.get("cmo_output") or {}
    cto = state.get("cto_output") or {}
    cfo = state.get("cfo_output") or {}

    # placeholder synthesis — replaced with LLM call later
    narrative = (
        f"Startup idea: {state.get('idea')}\n"
        f"Market: {cmo.get('tam', 'TBD')}\n"
        f"MVP: {cto.get('mvp_features', 'TBD')}\n"
        f"Funding ask: {cfo.get('funding_ask', 'TBD')}"
    )
    state["ceo_narrative"] = narrative
    return state