# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.db import Base, engine
from app.routers import dashboard

# routers
from app.whatsapp_webhook import router as whatsapp_router
from app.routers import expenses, stats, insights
from app.routers import categories

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(whatsapp_router)
app.include_router(expenses.router)
app.include_router(stats.router)
app.include_router(insights.router)
app.include_router(dashboard.router)
app.include_router(categories.router)


@app.get("/")
def health():
    return {"status": "running"}