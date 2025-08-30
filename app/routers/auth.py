
from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends
from utils.auth_utils import UserReg, get_current_user, get_password_hash

from dependencies import SessionDep
from database import  User


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/create-user/")
def create_user(user: UserReg, session: SessionDep) -> User:
    hashed_password = get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
    return current_user





