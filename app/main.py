from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, notify, notifier

app = FastAPI(title="Freight Delay Notifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Freight Delay Notifier API"}

app.include_router(health.router)
app.include_router(notify.router)
app.include_router(notifier.router)

