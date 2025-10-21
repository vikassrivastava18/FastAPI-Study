from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from utils.book_utils import BookRegister
from database.database import Book
from dependencies import SessionDep
from utils.auth_utils import get_current_active_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not Found"}}
)


# Create a new book
@router.post("/books")
async def register_book(book: BookRegister, 
                  session: SessionDep) -> Book:
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


# Get the list of all books
@router.get("/books")
async def book_list(sesion: SessionDep):
    return sesion.query(Book).all()


# Delete an existing book
@router.delete("/book/{book_id}")
async def delete_book(book_id: int, 
                session: SessionDep):
    book = session.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"detail": "Book deleted"}


# Update an existing book
@router.patch("/book/{book_id}")
async def update_book(book_id: int, 
                book: BookRegister, 
                session: SessionDep) -> Book:
    # Update an existing book by lookup with id and update book name
    updated_book = Book.model_validate(book)
    existing_book = session.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # update the book name (or other fields as needed)
    existing_book.name = updated_book.name

    session.add(existing_book)
    session.commit()
    session.refresh(existing_book)
    return existing_book


