from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.rag_routes import router as rag_router
from app.routes.repositories import router as repositories_router


app = FastAPI(
    title="RepoRAG API",
    description="AI GitHub Repository Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rag_router)
app.include_router(repositories_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }