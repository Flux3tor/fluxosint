from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3
from contextlib import contextmanager
from backend.engine.runner import run_modules

router = APIRouter()

class Target(BaseModel):
    type: str
    value: str

@contextmanager
def get_db():
    conn = sqlite3.connect("targets.db", timeout=30, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


@router.post("/targets/")
def create_target(target: Target):
    
    results = run_modules(target.type, target.value)

    with get_db() as db:
        cur = db.cursor()
        cur.execute("""
            INSERT INTO targets (type, value, risk_score)
            VALUES (?, ?, ?)
        """, (target.type, target.value, 0))

    return {
        "status": "ok",
        "results": results
    }
