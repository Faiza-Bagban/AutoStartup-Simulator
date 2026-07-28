"""LangGraph state machine wiring CEO -> [CMO|CTO|CFO stubs] -> CEO synthesize -> Investor."""
from langgraph.graph import StateGraph, END
from backend.orchestration.state import AgentState
from backend.agents.ceo_agent import parse_idea, synthesize
from backend.agents.investor_agent import select_questions, score_pitch


# --- stub nodes until Faiza/Lakshit/Sakshi wire real agents in ---
def cmo_stub(state: AgentState) -> AgentState:
    state["cmo_output"] = {"tam": "TBD - stub", "competitors": [], "persona": "TBD"}
    return state


def cto_stub(state: AgentState) -> AgentState:
    state["cto_output"] = {"mvp_features": "TBD - stub", "landing_page_url": None}
    return state


def cfo_stub(state: AgentState) -> AgentState:
    state["cfo_output"] = {"funding_ask": "TBD - stub", "revenue_model": "TBD"}
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("parse_idea", parse_idea)
    graph.add_node("cmo", cmo_stub)
    graph.add_node("cto", cto_stub)
    graph.add_node("cfo", cfo_stub)
    graph.add_node("synthesize", synthesize)
    graph.add_node("select_questions", select_questions)
    graph.add_node("score_pitch", score_pitch)

    graph.set_entry_point("parse_idea")

    # fan-out (parallel-ish — LangGraph runs these as separate edges from parse_idea)
    graph.add_edge("parse_idea", "cmo")
    graph.add_edge("parse_idea", "cto")
    graph.add_edge("parse_idea", "cfo")

    # fan-in
    graph.add_edge("cmo", "synthesize")
    graph.add_edge("cto", "synthesize")
    graph.add_edge("cfo", "synthesize")

    graph.add_edge("synthesize", "select_questions")
    graph.add_edge("select_questions", "score_pitch")
    graph.add_edge("score_pitch", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({"idea": "AI-powered plant disease detector for farmers"})
    print(result)