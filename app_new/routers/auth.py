from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response

from .utils.auth_utils import UserReg, get_password_hash, \
    Token, authenticate_user, create_access_token
from dependencies import SessionDep
from database import  User
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import SessionDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

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
    return Token(access_token=access_token, token_type="bearer")


@router.get("/secure-endpoint")
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"token": token}
