from fastapi import FastAPI

from app.routers import urls, redirect, auth

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="URL Shortener API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "https://flourishing-quokka-33cf66.netlify.app",
        "https://celebrated-paprenjak-9bad93.netlify.app",
        "https://playful-dragon-9acff8.netlify.app"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(urls.router)
app.include_router(redirect.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "message" : "URL Shortner API"
    }