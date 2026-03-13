def classify_signal(text):

    text = text.lower()

    if "blocked" in text or "blocker" in text:
        return "blocker"

    if "risk" in text or "failure" in text:
        return "risk"

    if "decision" in text:
        return "decision"

    if "dependency" in text:
        return "dependency"

    if "completed" in text or "success" in text:
        return "progress"

    return "progress"