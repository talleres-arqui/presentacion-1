from pydantic import BaseModel

class Publication(BaseModel):
    title: str
    body: str