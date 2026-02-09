from fastapi import APIRouter
from backend.db.database import get_db
from backend.engine.runner import run_modules

router = APIRouter(prefix="/targets", tags=["Targets"])

@router.post("/")
def create_target(target: dict):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO targets (type, value, risk_score)
        VALUES (?, ?, ?)
    """, (target["type"], target["value"], 0))

    target_id = cur.lastrowid

    results = run_modules(target["type"], target["value"])

    for r in results:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                module TEXT,
                data TEXT
            )
        """)
        cur.execute("""
            INSERT INTO results (target_id, module, data)
            VALUES (?, ?, ?)
        """, (target_id, r["module"], str(r["result"])))

    db.commit()

    return {
        "status": "scan complete",
        "results": results
    }
