import time
from datetime import datetime, timedelta
from db.database import get_db
from engine.runner import run_modules

CHECK_INTERVAL = 10

def run_scheduler():
    print("[SCHEDULER] Started")

    while True:
        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT id, target_id, interval, last_run FROM jobs")
        jobs = cur.fetchall()

        for job in jobs:
            job_id, target_id, interval, last_run = job

            should_run = False
            if not last_run:
                should_run = True
            else:
                last = datetime.fromisoformat(last_run)
                if datetime.now() - last >= timedelta(seconds=interval):
                    should_run = True

            if should_run:
                cur.execute("SELECT type, value FROM targets WHERE id = ?", (target_id,))
                target = cur.fetchone()

                if target:
                    print(f"[SCHEDULER] Running job {job_id} on {target[1]}")
                    run_modules(target[0], target[1])

                    cur.execute(
                        "UPDATE jobs SET last_run = ? WHERE id = ?",
                        (datetime.now().isoformat(), job_id)
                    )
                    db.commit()

        time.sleep(CHECK_INTERVAL)
