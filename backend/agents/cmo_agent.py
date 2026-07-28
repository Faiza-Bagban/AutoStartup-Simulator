"""
CMO Agent - Market Research & GTM Strategy
Owner: Faiza
"""
import json
from backend.models.llm_client import call_llm


class CMOAgent:
    def __init__(self):
        pass

    def analyze_market(self, idea: str) -> dict:
        """Estimate TAM/SAM/SOM for the given startup idea."""
        system = (
            "You are a market research analyst. Given a startup idea, "
            "estimate TAM, SAM, SOM in USD with 1-2 line reasoning each. "
            "Respond ONLY as JSON: {\"tam\": \"...\", \"sam\": \"...\", "
            "\"som\": \"...\", \"reasoning\": \"...\"}"
        )
        raw = call_llm(prompt=f"Startup idea: {idea}", system=system, temperature=0.3)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {"tam": "", "sam": "", "som": "", "reasoning": raw}

    # def scan_competitors(self, idea: str) -> list:
    #     """Search and summarize competitor landscape."""
    #     raise NotImplementedError

    def scan_competitors(self, idea: str) -> list:
        """Search and summarize competitor landscape."""
        from backend.tools.web_search import WebSearchTool
        searcher = WebSearchTool()
        results = searcher.search(f"competitors for {idea} startup", max_results=5)

        raw_context = "\n".join(
            f"- {r.get('title','')}: {r.get('content','')[:300]}" for r in results
        )
        system = (
            "You are a market analyst. Given raw search snippets about competitors, "
            "extract a list of distinct competitor names with a 1-line summary each. "
            "Respond ONLY as JSON list: [{\"name\": \"...\", \"summary\": \"...\"}]"
        )
        raw = call_llm(prompt=raw_context, system=system, temperature=0.3)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return [{"name": "parse_error", "summary": raw}]

    def generate_persona(self, idea: str) -> dict:
        """Generate target customer persona."""
        system = (
            "You are a UX researcher. Given a startup idea, create one primary "
            "target customer persona. Respond ONLY as JSON: "
            "{\"name\": \"...\", \"age_range\": \"...\", \"occupation\": \"...\", "
            "\"pain_points\": [\"...\"], \"motivations\": [\"...\"]}"
        )
        raw = call_llm(prompt=f"Startup idea: {idea}", system=system, temperature=0.5)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {"name": "", "age_range": "", "occupation": "", "pain_points": [], "motivations": [], "raw": raw}

    def generate_gtm_strategy(self, idea: str, market_data: dict) -> str:
        """Draft go-to-market strategy."""
        system = (
            "You are a startup growth strategist. Given a startup idea and its "
            "market data, write a concise go-to-market strategy (5-7 sentences) "
            "covering: initial channel, pricing approach, and early growth loop. "
            "Respond as plain text, no JSON."
        )
        prompt = f"Idea: {idea}\nMarket data: {json.dumps(market_data)}"
        return call_llm(prompt=prompt, system=system, temperature=0.6)
    
    def run(self, idea: str) -> dict:
        """Main entrypoint — orchestrates full CMO analysis."""
        market = self.analyze_market(idea)
        competitors = self.scan_competitors(idea)
        persona = self.generate_persona(idea)
        gtm = self.generate_gtm_strategy(idea, market)
        return {
            "market": market,
            "competitors": competitors,
            "persona": persona,
            "gtm_strategy": gtm,
        }