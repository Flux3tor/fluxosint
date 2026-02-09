from fastapi import FastAPI
from backend.api.targets import router as target_router
from backend.api.leakguard import router as leakguard_router
from backend.api.jobs import router as jobs_router

app = FastAPI(title="FluxOSINT")

app.include_router(target_router)
app.include_router(leakguard_router)

def api_status():
    return {"status": "FluxOSINT API online"}

app.include_router(jobs_router)