from fastapi import FastAPI

from database import create_db_and_tables
from routers import auth, web
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

# Define a welcome user root URL
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

