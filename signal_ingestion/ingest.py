import uuid
import datetime
from models.signal import Signal


def fetch_slack_signals():

    signals = [
        Signal(
            id=str(uuid.uuid4()),
            source="slack",
            timestamp=datetime.datetime.utcnow().isoformat(),
            team="backend",
            raw_content="API deployment blocked due to authentication service outage"
        ),

        Signal(
            id=str(uuid.uuid4()),
            source="slack",
            timestamp=datetime.datetime.utcnow().isoformat(),
            team="data",
            raw_content="Weekly analytics pipeline completed successfully"
        )
    ]

    return signals


def fetch_github_signals():

    signals = [
        Signal(
            id=str(uuid.uuid4()),
            source="github",
            timestamp=datetime.datetime.utcnow().isoformat(),
            team="frontend",
            raw_content="Bug: dashboard crashes when loading signal feed"
        )
    ]

    return signals


def ingest_signals():

    signals = []
    signals.extend(fetch_slack_signals())
    signals.extend(fetch_github_signals())

    return signals