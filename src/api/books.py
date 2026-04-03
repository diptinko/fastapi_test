from fastapi import APIRouter
from sqlalchemy import select

from src.api.dependencies import SessionDep
from src.database import Base, engine
from src.models.books import BookModel
from src.schemas.books import BookAddSchema

router = APIRouter()


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

    
@router.post("/books")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@router.get("/books")
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()
    print(f"{books=}")
    return books