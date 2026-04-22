from pydantic import BaseModel
from typing import List

class EntityRequest(BaseModel):
    name: str
    business_type: str
    location: str

class EntityResponse(BaseModel):
    primary_entity: str
    brand: str
    location: str
    services: List[str]
    industry: List[str]
    audience: List[str]
    related_entities: List[str]