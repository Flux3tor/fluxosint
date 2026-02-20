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

    from datetime import datetime
    import json
    
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO targets (type, value, risk_score)
        VALUES (?, ?, ?)
    """, (target.type, target.value, overall_risk))

    target_id = cur.lastrowid

    cur.execute("""
        INSERT INTO scans (target_id, overall_risk, created_at)
        VALUES (?, ?, ?)
    """, (target_id, overall_risk, datetime.now().isoformat()))

    scan_id = cur.lastrowid

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
        SELECT s.id, s.overall_risk, s.created_at
        FROM scans s
        WHERE s.target_id = ?
        ORDER BY s.created_at DESC
    """, (target_id,))

    scans = cur.fetchall()

    history = []

    for scan in scans:
        scan_id, overall_risk, created_at = scan

        cur.execute("""
            SELECT module_name, data, risk
            FROM scan_results
            WHERE scan_id = ?
        """, (scan_id,))

        modules = cur.fetchall()

        history.append({
            "scan_id": scan_id,
            "overall_risk": overall_risk,
            "created_at": created_at,
            "modules": [
                {
                    "module": m[0],
                    "data": json.loads(m[1]),
                    "risk": m[2]
                }
                for m in modules
            ]
        })

    db.close()
    return history