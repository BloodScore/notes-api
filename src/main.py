from fastapi import FastAPI

from src.notes import routes


app = FastAPI()

app.include_router(routes.boards_router)
app.include_router(routes.notes_router)


