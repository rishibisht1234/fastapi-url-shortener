from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.routers import urls, redirect
from app.database.connections import get_db
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate, URLResponse
from app.services.url_service import create_short_url
from app.core.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="URL Shortener API")
app.include_router(urls.router)
app.include_router(redirect.router)

@app.get("/")
def home():
    return {
        "message" : "URL Shortner API"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "https://your-site.netlify.app"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)