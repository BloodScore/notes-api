from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class InDB(BaseModel):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class RouteResponse(BaseModel):
    message: str


class NoteInDB(InDB):
    text: str
    views_count: int
    desk_id: int


class BoardInDB(InDB):
    title: str
    notes: Union[List[NoteInDB], None] = None


class BoardResponse(RouteResponse):
    board: BoardInDB
