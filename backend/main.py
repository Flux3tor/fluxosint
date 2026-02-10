from fastapi import FastAPI
from backend.api.targets import router as target_router
from backend.api.leakguard import router as leakguard_router
from backend.api.jobs import router as jobs_router

app = FastAPI()

app.include_router(target_router)
app.include_router(leakguard_router)
<<<<<<< HEAD
app.include_router(jobs_router)
=======

def api_status():
    return {"status": "FluxOSINT API online"}

app.include_router(jobs_router)
>>>>>>> 0d5fb4fa3e95f7e1d21b53737c678fb9057b5338
