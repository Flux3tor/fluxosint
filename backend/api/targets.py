from fastapi import APIRouter
from pydantic import BaseModel
from backend.db.database import get_db
from backend.engine.runner import run_modules

router = APIRouter()

class Target(BaseModel):
    type: str
    value: str


@router.post("/targets/")
def create_target(target: Target):

    results = run_modules(target.type, target.value)

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO targets (type, value, risk_score)
        VALUES (?, ?, ?)
    """, (target.type, target.value, 0))

    db.commit()
    db.close()

    return {
        "status": "ok",
        "results": results
    }