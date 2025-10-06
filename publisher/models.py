from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from database import Base

class PublicationDB(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)


class Publication(BaseModel):
    id: int | None = None
    title: str
    body: str

    class Config:
        orm_mode = True
