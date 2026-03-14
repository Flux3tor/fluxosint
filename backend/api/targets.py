from fastapi import APIRouter
from pydantic import BaseModel
from backend.db.database import get_db
from backend.engine.runner import run_modules
from datetime import datetime
import json

router = APIRouter()

class Target(BaseModel):
    type: str
    value: str

@router.post("/targets/")
def create_target(target: Target):

    results = run_modules(target.type, target.value)
    overall_risk = sum(mod["result"]["risk"] for mod in results)

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id FROM targets WHERE type=? AND value=?",
        (target.type, target.value)
    )
    existing = cur.fetchone()

    if existing:
        target_id = existing[0]
    else:
        cur.execute(
            "INSERT INTO targets (type,value,risk_score) VALUES (?,?,?)",
            (target.type, target.value, overall_risk)
        )
        target_id = cur.lastrowid

    cur.execute(
        "INSERT INTO scans (target_id,overall_risk,created_at) VALUES (?,?,?)",
        (target_id, overall_risk, datetime.now().isoformat())
    )
    scan_id = cur.lastrowid

    for mod in results:
        cur.execute(
            "INSERT INTO scan_results (scan_id,module_name,data,risk) VALUES (?,?,?,?)",
                (
                    scan_id,
                    mod["module"],
                    json.dumps(mod["result"]["data"]),
                    mod["result"]["risk"]
                )
        )
    
    db.commit()
    db.close()

    return {
        "status": "ok",
        "target_id": target_id,
        "overall_risk": overall_risk,
        "results": results
    }

@router.get("/targets")
def get_targets():

    db = get_db()

    cur = db.cursor()

    cur.execute("""
        SELECT id,type,value,risk_score
        FROM targets
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    db.close()

    return [
        {
            "id": r[0],
            "type": r[1],
            "value": r[2],
            "risk": r[3]
        }
        for r in rows
    ]

@router.get("/targets/{target_id}/history")
def get_history(target_id: int):

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id,overall_risk,created_at
        FROM scans
        WHERE target_id=?
        ORDER BY created_at DESC
    """,(target_id,))

    scans = cur.fetchall()

    history=[]

    for scan in scans:

        scan_id, risk, created = scan

        cur.execute("""
            SELECT module_name,data,risk
            FROM scan_results
            WHERE scan_id=?
        """,(scan_id,))

        modules = cur.fetchall()
        
        history.append({
            "scan_id": scan_id,
            "overall_risk": risk,
            "created_at": created,
            "modules":[
                {
                    "module":m[0],
                }
                for m in modules
            ]
        })

    db.close()
    return history