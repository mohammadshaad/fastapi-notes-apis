from pydantic import BaseModel

class Note(BaseModel):
    id: int
    title: str
    description: str
    important: bool

    class Config:
        orm_mode = True