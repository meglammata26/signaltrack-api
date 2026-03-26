from sqlalchemy.orm import Session
from db_models import Signal, Insight


def create_signal(db: Session, data: dict):
    signal = Signal(**data)
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal


def get_signals(db: Session):
    return db.query(Signal).all()


def create_insight(db: Session, data: dict):
    insight = Insight(**data)
    db.add(insight)
    db.commit()
    db.refresh(insight)
    return insight


def get_insights(db: Session):
    return db.query(Insight).all()