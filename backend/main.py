from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.api.targets import router as target_router
from backend.api.leakguard import router as leakguard_router
from backend.api.jobs import router as jobs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(target_router)
app.include_router(leakguard_router)
app.include_router(jobs_router)
