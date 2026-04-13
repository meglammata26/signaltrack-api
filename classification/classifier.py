# classification/classifier.py

def classify_signal(text):
    text = text.lower()

    BLOCKER_KEYWORDS = [
        "blocked", "blocker", "can't proceed", "cannot proceed",
        "stuck", "halted", "broken", "down", "outage", "timeout",
        "api timeout", "not working", "failing", "failed to connect"
    ]
    RISK_KEYWORDS = [
        "risk", "failure", "warning", "unstable", "degraded",
        "slow", "latency", "memory leak", "overload", "spike",
        "flaky", "inconsistent", "concerning"
    ]
    DECISION_KEYWORDS = [
        "decision", "approve", "should we", "what do we do",
        "need alignment", "agreed", "voted", "decided"
    ]
    DEPENDENCY_KEYWORDS = [
        "dependency", "depends on", "waiting on", "blocked by",
        "needs", "requires", "pending review", "external team"
    ]
    PROGRESS_KEYWORDS = [
        "completed", "success", "deployed", "shipped", "merged",
        "done", "resolved", "fixed", "closed", "released"
    ]

    for kw in BLOCKER_KEYWORDS:
        if kw in text: return "blocker"
    for kw in RISK_KEYWORDS:
        if kw in text: return "risk"
    for kw in DECISION_KEYWORDS:
        if kw in text: return "decision"
    for kw in DEPENDENCY_KEYWORDS:
        if kw in text: return "dependency"
    for kw in PROGRESS_KEYWORDS:
        if kw in text: return "progress"

    return "progress"