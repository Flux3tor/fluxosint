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

    overall_risk = sum(mod["result"]["risk"] for mod in results)

    import json
    from datetime import datetime
    
    for mod in results:
        cur.execute("""
            INSERT INTO scan_results (target_id, module, data, risk, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            target_id,
            mod["module"],
            json.dumps(mod["result"]["data"]),
            mod["result"]["risk"],
            datetime.now().isoformat()
        ))

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO targets (type, value, risk_score)
        VALUES (?, ?, ?)
    """, (target.type, target.value, overall_risk))
    target_id = cur.lastrowid

    from datetime import datetime
    
    cur.execute("""
        INSERT INTO scans (target_id, overall_risk, created_at)
        VALUES (?, ?, ?)
    """, (target_id, overall_risk, datetime.now().isoformat()))

    scan_id = cur.lastrowid

    import json

    for mod in results:
        cur.execute("""
        INSERT INTO scan_results (scan_id, module_name, data, risk)
            VALUES (?, ?, ?, ?)
        """, (
            scan_id,
            mod["module"],
            json.dumps(mod["result"]["data"]),
            mod["result"]["risk"]
        ))

    db.commit()
    db.close()

    return {
        "status": "ok",
        "overall_risk": overall_risk,
        "results": results
    }

@router.get("/targets/{target_id}/history")
def get_history(target_id: int):
    db = get_db()
    cur = db.cursor()

    import json

    cur.execute("""
        SELECT module_name, data, risk, created_at
        FROM scan_results
        WHERE target_id = ?
        ORDER BY created_at DESC
    """, (target_id,))

    rows = cur.fetchall()

    return [
        {
            "module": r[0],
            "data": json.loads(r[1]),
            "risk": r[2],
            "created_at": r[3]
        }
        for r in rows
    ]