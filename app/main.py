from typing import Annotated

from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlmodel import  select

from db import create_db_and_tables, Hero, User
from auth import Token, UserReg, authenticate_user, \
                 create_access_token, get_current_active_user, \
                 get_password_hash
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from deps import SessionDep


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/register/")
def register_user(user: UserReg, session: SessionDep) -> User:
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
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
    return current_user


@app.get("/heros/", response_class=HTMLResponse)
def read_heros(
    request: Request,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heros = session.exec(select(Hero).offset(offset).limit(limit)).all()
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("heroes.html", {"request": request, "heros": heros})

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep,
                current_user: Annotated[User, Depends(get_current_active_user)]) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


