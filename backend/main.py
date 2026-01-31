from fastapi import FastAPI
from api.targets import router as target_router

app = FastAPI(title="FluxOSINT")

app.include_router(target_router)

@app.get("/")
def home():
    return {"status": "FluxOSINT online"}
