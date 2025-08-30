from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from .utils.auth_utils import get_password_hash, \
    Token, authenticate_user, create_access_token
from .utils.auth_utils import get_current_user_web
from dependencies import SessionDep
from database import User as UserModel
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/web",
    tags=["web"],
    # dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


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


@router.get("/")
async def home(user: Annotated[UserModel, Depends(get_current_user_web)]):
    return HTMLResponse(content=open("templates/heroes.html").read())


@router.get("/login")
async def login_user():
    return HTMLResponse(content=open("templates/login.html").read())


@router.get("/{item_id}")
async def read_item(item_id: str, user: Annotated[UserModel, Depends(get_current_user_web)]):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


