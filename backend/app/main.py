
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.comparison import (
    router as comparison_router
)

from backend.app.routes.documents import (
    router as documents_router
)

from backend.app.routes.query import (
    router as query_router
)


app = FastAPI(
    title="LegalDoc-AI",
    description=(
        "Indian Legal Research and "
        "Document Intelligence API"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    documents_router
)

app.include_router(
    query_router
)

app.include_router(comparison_router)

@app.get("/")
def root():

    return {
        "message": "LegalDoc-AI API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

