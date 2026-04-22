from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="SEO AI Engine")

app.include_router(router)