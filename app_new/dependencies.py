from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from fastapi import Header, HTTPException

from database import get_session


SessionDep = Annotated[Session, Depends(get_session)]
