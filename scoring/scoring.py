# scoring/scoring.py

def score_signal(content: str):
    text = content.lower()

    IMPACT_KEYWORDS = {
        "production": 40, "outage": 45, "down": 35, "data loss": 50,
        "blocked": 30, "broken": 30, "critical": 40, "failed": 25,
        "deployed": 15, "merged": 10, "resolved": 5
    }
    URGENCY_KEYWORDS = {
        "now": 30, "immediately": 40, "urgent": 35, "asap": 35,
        "today": 20, "blocking": 30, "timeout": 25, "outage": 40,
        "down": 30, "critical": 35, "p0": 45, "p1": 30, "blocking": 30,
        "failed": 20, "broken": 25,"cannot proceed": 35,"latency": 15,"spiked": 20,
        "memory": 10, "merged": 5,
    }

    impact  = sum(v for k, v in IMPACT_KEYWORDS.items()  if k in text)
    urgency = sum(v for k, v in URGENCY_KEYWORDS.items() if k in text)

    return float(min(impact, 100)), float(min(urgency, 100))