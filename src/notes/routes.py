from fastapi import APIRouter, Depends

from src.database import Session, get_db_session
from src.notes.models import Board, Note
from src.notes.schemas import BoardResponse

notes_router = APIRouter(
    prefix='/notes',
    tags=['notes']
)

boards_router = APIRouter(
    prefix='/boards',
    tags=['boards']
)


@boards_router.post('/create', response_model=BoardResponse)
async def create_board(board_title: str, db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    board = Board.create(title=board_title)

    return {'message': 'Board successfully created', 'board': board}
