from fastapi import APIRouter, HTTPException, status
from typing import Annotated
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import SessionDep
from database import  User
from auth import Token, UserReg, authenticate_user, \
                 create_access_token, get_current_active_user, \
                 get_password_hash


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/create-user/")
def create_user(user: UserReg, session: SessionDep) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        disabled=user.disabled,
        hashed_password=hashed_password
    )
    db_user = User.validate(db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
    return current_user





