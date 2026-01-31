from fastapi import APIRouter
from db.database import get_db

router = APIRouter(prefix="/targets", tags=["Targets"])

@router.post("/")
def create_target(target: dict):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO targets (type, value, risk_score)
        VALUES (?, ?, ?)
    """, (target["type"], target["value"], 0))

    db.commit()
    return {"status": "target added"}
