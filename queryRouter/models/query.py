from pydantic import BaseModel
from typing import Optional

class ParsedQuery(BaseModel):
    keyword: str
    payload: Optional[str] = None
    raw_query: str

class Shortcut(BaseModel):
    url: str
    search: Optional[str] = None