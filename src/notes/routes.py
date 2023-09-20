from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status

from src.database import Session, get_db_session
from src.notes.models import Board, Note
from src.notes.schemas import BoardResponse, NoteResponse, BoardListResponse, NoteListResponse

notes_router = APIRouter(
    prefix='/notes',
    tags=['notes']
)

boards_router = APIRouter(
    prefix='/boards',
    tags=['boards']
)


def _get_board(board_id: int) -> Board:
    board = Board.get(id=board_id)

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Board not found')

    return board


def _get_note(note_id: int) -> Note:
    note = Note.get(id=note_id)

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')

    return note


@boards_router.post('', response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(board_title: str, db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    board = Board.create(title=board_title)

    return {'message': 'Board created', 'board': board}


@boards_router.get('', response_model=BoardListResponse, status_code=status.HTTP_200_OK)
async def get_boards_list(db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    boards = Board.get_all()

    return {'message': 'Boards list', 'boards': boards}


@boards_router.get('/{board_id}', response_model=BoardResponse, status_code=status.HTTP_200_OK)
async def get_specific_board(board_id: int, db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    board = _get_board(board_id)

    return {'message': 'Board found', 'board': board}


@boards_router.put('/{board_id}', response_model=BoardResponse, status_code=status.HTTP_200_OK)
async def update_board(board_id: int, board_title: str, db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    board = _get_board(board_id)

    board.update(title=board_title)

    return {'message': 'Board updated', 'board': board}


@boards_router.delete('/{board_id}', status_code=status.HTTP_200_OK)
async def delete_board(board_id: int, db_session: Session = Depends(get_db_session)):
    Board.set_db_session(db_session)

    board = _get_board(board_id)

    board.delete()

    return {'message': 'Board deleted'}


@boards_router.put('/pin-note/{board_id}', response_model=BoardResponse, status_code=status.HTTP_200_OK)
async def pin_note_to_board(board_id: int, note_id: int, db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)
    Board.set_db_session(db_session)

    note = _get_note(note_id)
    board = _get_board(board_id)

    note.update(board=board)

    return {'message': f'Pinned note {note.id} to board {board.id}', 'board': board}


@boards_router.put('/unpin-note/{board_id}', response_model=BoardResponse, status_code=status.HTTP_200_OK)
async def unpin_note_from_board(board_id: int, note_id: int, db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)
    Board.set_db_session(db_session)

    note = _get_note(note_id)
    board = _get_board(board_id)

    if note.board_id != board.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Note {note.id} doesn\'t attached to board {board.id}')

    note.update(board=None)

    return {'message': f'Note {note.id} unpinned from board {board.id}', 'board': board}


@notes_router.post('', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(text: str, board_id: Union[int, None] = None, db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)

    if board_id:
        Board.set_db_session(db_session)
        board = _get_board(board_id)
        note = Note.create(text=text, board=board)
    else:
        note = Note.create(text=text)

    return {'message': 'Note created', 'note': note}


@notes_router.get('', response_model=NoteListResponse, status_code=status.HTTP_200_OK)
async def get_notes_list(db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)

    notes = Note.get_all()

    return {'message': 'Notes list', 'notes': notes}


@notes_router.get('/{note_id}', response_model=NoteResponse, status_code=status.HTTP_200_OK)
async def get_specific_note(note_id: int, db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)

    note = _get_note(note_id)
    note.update(views_count=note.views_count + 1)

    return {'message': 'Note found', 'note': note}


@notes_router.put('/{note_id}', response_model=NoteResponse, status_code=status.HTTP_200_OK)
async def update_note(note_id: int, note_text: Union[str, None] = None, board_id: Union[int, None] = None,
                      db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)

    note = _get_note(note_id)

    if board_id:
        Board.set_db_session(db_session)
        board = _get_board(board_id)
        if note.board_id != board.id:
            note.board = board

    if note_text:
        note.text = note_text

    note.save()

    return {'message': 'Note updated', 'note': note}


@notes_router.delete('/{note_id}', status_code=status.HTTP_200_OK)
async def delete_note(note_id: int, db_session: Session = Depends(get_db_session)):
    Note.set_db_session(db_session)

    note = _get_note(note_id)

    note.delete()

    return {'message': 'Note deleted'}
