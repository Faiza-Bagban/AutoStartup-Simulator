# Agent Roles

## CEO-agent (Yeshita) — backend/agents/ceo_agent.py
- parse_idea: validates/cleans raw idea input
- synthesize: combines CMO+CTO+CFO outputs into narrative (LLM-based synthesis pending Wk3)

## Investor-agent (Yeshita) — backend/agents/investor_agent.py
- select_questions: picks questions from data/question_bank.json
- score_pitch: scores 0-10 based on Q&A (stub — real LLM scoring pending Wk8)

## CMO-agent (Faiza) — backend/agents/cmo_agent.py
- Status: skeleton + web_search integrated (Wk1). Full v1 in progress.

## CFO-agent (Sakshi) — backend/agents/cfo_agent.py
- Status: skeleton done (Wk1). Revenue model + unit economics in progress.

## CTO-agent (Lakshit) — backend/agents/cto_agent.py
- Status: NOT STARTED. Currently stubbed in graph.py (cto_stub). Lakshit starts Week 5.

## Orchestration (Yeshita) — backend/orchestration/graph.py
- Fan-out: parse_idea -> [cmo, cto, cfo] (parallel)
- Fan-in: [cmo, cto, cfo] -> synthesize -> select_questions -> score_pitch -> END