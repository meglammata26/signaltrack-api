# api/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from classification.classifier import classify_signal
from scoring.scoring import score_signal
from insight_engine.llm_analysis import generate_insight
from database import SessionLocal, engine, Base
import db_models, schemas, crud
import datetime
import traceback


# --- Helper ---
def cluster_signal(content: str, type_: str):
    return type_


# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ROUTES ---

@app.post("/signals")
def create_signal(signal: schemas.SignalCreate, db: Session = Depends(get_db)):
    try:
        # --- classification ---
        try:
            type_ = classify_signal(signal.content)
        except Exception:
            type_ = "unknown"

        # --- scoring (FIXED) ---
        try:
            impact, urgency = score_signal(signal.content)
            impact = float(impact)
            urgency = float(urgency)
        except Exception:
            impact, urgency = 0.0, 0.0

        # --- clustering ---
        cluster_id = cluster_signal(signal.content, type_)

        # --- summary ---
        summary = signal.content[:100]

        # --- save signal ---
        db_signal = crud.create_signal(db, {
            "source": signal.source,
            "timestamp": datetime.datetime.utcnow(),
            "content": signal.content,
            "summary": summary,
            "type": type_,
            "impact_score": impact,
            "urgency_score": urgency,
            "cluster_id": cluster_id
        })

        # --- generate insight ---
        try:
            insight_text = generate_insight(signal.content)
        except Exception:
            insight_text = "Insight generation failed"

        # --- save insight ---
        crud.create_insight(db, {
            "cluster_id": cluster_id,
            "summary": insight_text,
            "status": "pending"
        })

        return {
    "id": db_signal.id,
    "source": db_signal.source,
    "summary": db_signal.summary,
    "type": db_signal.type,
    "impact_score": db_signal.impact_score,
    "urgency_score": db_signal.urgency_score,
    "cluster_id": db_signal.cluster_id
}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


@app.get("/signals", response_model=list[schemas.SignalResponse])
def get_signals(db: Session = Depends(get_db)):
    return crud.get_signals(db)


@app.get("/insights", response_model=list[schemas.InsightResponse])
def get_insights(db: Session = Depends(get_db)):
    return crud.get_insights(db)