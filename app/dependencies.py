from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from fastapi import Header, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database import get_session


SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_token_header(x_token: Annotated[str, Header()]):
    print("Token::", x_token)
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")