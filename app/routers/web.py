from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

from utils.auth_utils import get_current_user_web
from database import User as UserModel

router = APIRouter(
    prefix="/web",
    tags=["web"],
    # dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


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