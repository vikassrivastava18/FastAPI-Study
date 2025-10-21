from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from utils.auth_utils import (Token,
                              authenticate_user,
                              create_access_token,
                              get_current_user_web)

from dependencies import SessionDep
from database.database import User as UserModel
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/web",
    tags=["web"],
    responses={404: {"description": "Not found"}},
)


"""Create access token for the web"""
@router.post("/token")
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


"""Home page, accessible only to authenticated users."""
@router.get("/")
async def home(user: Annotated[UserModel,
               Depends(get_current_user_web)]
               ):
    return HTMLResponse(content=open("templates/heroes.html").read())


"""Login page"""
@router.get("/login")
async def login_user():
    return HTMLResponse(content=open("templates/login.html").read())





