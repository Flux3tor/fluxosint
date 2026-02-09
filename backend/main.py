from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.targets import router as target_router
from api.leakguard import router as leakguard_router
from api.jobs import router as jobs_router

app = FastAPI(title="FluxOSINT")

app.include_router(target_router)
app.include_router(leakguard_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api")
def api_status():
    return {"status": "FluxOSINT API online"}

app.include_router(jobs_router)