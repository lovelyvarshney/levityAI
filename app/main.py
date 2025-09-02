from fastapi import FastAPI
from app.routes import health, notify, notifier

app = FastAPI(title="Freight Delay Notifier")

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome to Freight Delay Notifier API"}

app.include_router(health.router)
app.include_router(notify.router)
app.include_router(notifier.router)

