from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import products, recommend
import os

app = FastAPI(title="Mini Product Search & Recommendation")

# Allow CORS for local development (frontend demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static frontend directly via FastAPI to avoid needing a separate static server
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Simple route to open the demo
@app.get("/demo")
def demo():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(recommend.router, prefix="", tags=["recommend"])

@app.get("/")
def root():
    return {"message": "Welcome to Mini Product Search & Recommendation System"}
