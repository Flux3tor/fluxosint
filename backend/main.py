from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.targets import router as target_router
from backend.db.base import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    print("Initializing database...")
    init_db()

app.include_router(target_router)
