from pydantic import BaseModel
from typing import List, Optional

class EntityRequest(BaseModel):
    keyword: Optional[str] = None
    web_url: Optional[str] = None
    location: Optional[str] = None

class EntityResponse(BaseModel):
    primary_entity: str
    brand: str
    location: str
    services: List[str]
    industry: List[str]
    audience: List[str]
    related_entities: List[str]