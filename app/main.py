from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import create_db_and_tables
from routers import auth, web
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import SessionDep
from utils.auth_utils import Token, authenticate_user, create_access_token
from fastapi.responses import Response


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(web.router, include_in_schema=False)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep
    ) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if "text/html" in form_data.scopes:
        response = Response()
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.headers["Location"] = "/web/"
        response.status_code = status.HTTP_303_SEE_OTHER
        return response
    return Token(access_token=access_token, token_type="bearer")




