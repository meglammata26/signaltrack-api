from dataclasses import dataclass
from typing import List


@dataclass
class Signal:
    id: str
    source: str
    timestamp: str
    team: str

    raw_content: str
    content_summary: str = ""

    signal_type: str = ""

    impact_score: int = 0
    urgency_score: int = 0
    confidence_score: float = 0.0

    owner: str = ""
    status: str = "active"

    related_signals: List[str] = None