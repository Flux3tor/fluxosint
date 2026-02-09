from fastapi import APIRouter
from db.database import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/")
def create_job(job: dict):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO jobs (target_id, interval, last_run)
        VALUES (?, ?, ?)
    """, (job["target_id"], job["interval"], None))

    db.commit()
    return {"status": "job scheduled"}
