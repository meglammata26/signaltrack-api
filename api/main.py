# api/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from classification.classifier import classify_signal
from scoring.scoring import score_signal
from insight_engine.llm_analysis import generate_insight
from database import SessionLocal, engine, Base
import db_models, schemas, crud
import datetime
import traceback
import json

# --- CREATE APP ---
app = FastAPI(title="SignalTrack API")

# --- CORS (allow frontend connection) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HELPER FUNCTION ---

def cluster_signal(content: str, type_: str):
    text = content.lower()

    CLUSTERS = {
        "auth":       ["auth", "login", "oauth", "token", "permission", "access"],
        "deployment": ["deploy", "pipeline", "ci", "cd", "build", "release", "merge"],
        "api":        ["api", "endpoint", "timeout", "request", "response", "gateway"],
        "database":   ["database", "db", "query", "migration", "schema", "postgres", "sqlite"],
        "payments":   ["payment", "stripe", "billing", "transaction", "checkout"],
        "infra":      ["server", "memory", "cpu", "latency", "load", "crash", "infra"],
    }

    for cluster, keywords in CLUSTERS.items():
        if any(kw in text for kw in keywords):
            return cluster

    return type_  # fallback to signal type

# --- CREATE DB TABLES ---
Base.metadata.create_all(bind=engine)

# --- DB DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.post("/signals", response_model=schemas.SignalResponse)
def create_signal(signal: schemas.SignalCreate, db: Session = Depends(get_db)):
    try:
        # --- classification ---
        try:
            type_ = classify_signal(signal.content)
        except Exception:
            type_ = "unknown"

        # --- scoring ---
        try:
            impact, urgency = score_signal(signal.content)
            impact = float(impact)
            urgency = float(urgency)
        except Exception:
            impact, urgency = 0.0, 0.0

        # --- clustering ---
        cluster_id = cluster_signal(signal.content, type_)

        # --- summary (first 100 chars) ---
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
            insight_data = generate_insight(signal.content)
        except Exception:
            insight_data = {"error": "Insight generation failed"}

        # --- ensure insight_data is a string before saving ---
        insight_summary = insight_data if isinstance(insight_data, str) else json.dumps(insight_data)

        # --- save insight ---
        crud.create_insight(db, {
            "cluster_id": cluster_id,
            "summary": insight_summary,
            "status": "pending"
        })

        return schemas.SignalResponse(
    id=db_signal.id,
    source=db_signal.source,
    timestamp=db_signal.timestamp,
    summary=db_signal.summary,
    type=db_signal.type,
    impact_score=db_signal.impact_score,
    urgency_score=db_signal.urgency_score,
    cluster_id=db_signal.cluster_id
)

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/signals", response_model=list[schemas.SignalResponse])
def get_signals(db: Session = Depends(get_db)):
    return crud.get_signals(db)

@app.get("/insights", response_model=list[schemas.InsightResponse])
def get_insights(db: Session = Depends(get_db)):
    return crud.get_insights(db)

# --- /analyze endpoint ---
class SignalRequest(BaseModel):
    signals: list

@app.post("/analyze")
def analyze_signals(request: SignalRequest):
    try:
        result = generate_insight(request.signals)
        return result
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    
#connect to approve and publish
@app.patch("/insights/{insight_id}/approve")
def approve_insight(insight_id: int, db: Session = Depends(get_db)):
    insight = db.query(db_models.Insight).filter(db_models.Insight.id == insight_id).first()
    if not insight:
        return {"error": "Insight not found"}
    insight.status = "approved"
    db.commit()
    db.refresh(insight)
    return {"id": insight.id, "status": insight.status}