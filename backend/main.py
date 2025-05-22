from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import query_router, scrape_router, clear_router, health_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router.router, prefix="/api")
app.include_router(scrape_router.router, prefix="/api")
app.include_router(clear_router.router, prefix="/api")
app.include_router(health_router.router, prefix="/api")
