from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String)
    summary = Column(String)
    type = Column(String)

    impact_score = Column(Float)
    urgency_score = Column(Float)

    cluster_id = Column(String)


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(String)
    summary = Column(String)
    status = Column(String, default="pending")  # pending, approved