def score_signal(signal_type):

    scoring_table = {

        "blocker": {
            "impact": 90,
            "urgency": 95
        },

        "risk": {
            "impact": 80,
            "urgency": 85
        },

        "decision": {
            "impact": 70,
            "urgency": 70
        },

        "dependency": {
            "impact": 60,
            "urgency": 65
        },

        "progress": {
            "impact": 40,
            "urgency": 30
        }
    }

    return scoring_table.get(
        signal_type,
        {"impact": 50, "urgency": 50}
    )