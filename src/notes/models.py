from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Note(BaseModel):
    __tablename__ = 'notes'

    text = Column(Text)
    views_count = Column(Integer, default=0)

    board_id = Column(ForeignKey('boards.id', ondelete='CASCADE'))
    board = relationship('Board', back_populates='notes')


class Board(BaseModel):
    __tablename__ = 'boards'

    title = Column(String(255))

    notes = relationship('Note', back_populates='board', cascade='all, delete', passive_deletes=True)
