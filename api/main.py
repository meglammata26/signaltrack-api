from fastapi import FastAPI
from typing import List

from signal_ingestion.ingest import ingest_signals
from classification.classifier import classify_signal
from scoring.scoring import score_signal
from models.signal import Signal

app = FastAPI()


@app.get("/signals", response_model=List[Signal])
def get_signals():

    signals = ingest_signals()

    for signal in signals:

        signal_type = classify_signal(signal.raw_content)

        scores = score_signal(signal_type)

        signal.signal_type = signal_type
        signal.impact_score = scores["impact"]
        signal.urgency_score = scores["urgency"]

    return signals

@app.get("/analytics")
def get_signal_analytics():

    signals = ingest_signals()

    counts = {
        "blocker": 0,
        "risk": 0,
        "decision": 0,
        "dependency": 0,
        "progress": 0
    }

    for signal in signals:

        signal_type = classify_signal(signal.raw_content)
        counts[signal_type] += 1

    return {
        "total_signals": len(signals),
        "signal_distribution": counts
    }