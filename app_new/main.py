from fastapi import FastAPI

from database.database import create_db_and_tables
from routers import auth, web, books
from config import ACCESS_TOKEN_EXPIRE_MINUTES


"""
Instantiate a FastAPI app object, which you use to define routes and run your API server.
"""
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(web.router, include_in_schema=False)
app.include_router(books.router)



