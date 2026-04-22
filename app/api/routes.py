from fastapi import APIRouter
from app.schemas.entity_schema import EntityRequest  
from app.services.entity_service  import generate_entities
router = APIRouter()

@router.get("/")
def root():
    return {"message": "SEO AI Engine Running"}

@router.post("/entity/generate")
def create_entities(request: EntityRequest):
    return generate_entities(request)