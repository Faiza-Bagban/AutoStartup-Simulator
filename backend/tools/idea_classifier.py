"""Rule-based idea-category classifier — keeps demo reliable, no extra LLM call needed.
Categories scoped down to 4 per project decision: saas, marketplace, mobile_app, consumer."""

CATEGORY_KEYWORDS = {
    "saas": ["dashboard", "platform", "workflow", "b2b", "analytics", "tool", "software", "api"],
    "marketplace": ["marketplace", "buyers", "sellers", "connect", "listing", "booking", "rental"],
    "mobile_app": ["app", "mobile", "on-the-go", "notification", "tracker"],
    "consumer": ["subscription", "box", "product", "consumer", "delivery", "lifestyle"],
}


def classify_idea(idea: str) -> str:
    idea_lower = idea.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in idea_lower:
                scores[cat] += 1

    best_cat = max(scores, key=scores.get)
    return best_cat if scores[best_cat] > 0 else "saas"  # default fallback