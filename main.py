from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import reports, dFrames, stat, utils


app = FastAPI()
app.include_router(reports.router)
app.include_router(dFrames.router)
app.include_router(stat.router)
app.include_router(utils.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def hello():
    return {'data':'Hi'}