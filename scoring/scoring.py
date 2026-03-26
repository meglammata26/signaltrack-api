# scoring/scoring.py

def score_signal(content: str):
    """
    Returns (impact_score, urgency_score) as floats
    """

    try:
        # Simple heuristic scoring (you can improve later)
        length = len(content)

        impact = min(100, length * 0.5)     # scale to max 100
        urgency = min(100, length * 0.3)

        return float(impact), float(urgency)

    except Exception:
        return 0.0, 0.0