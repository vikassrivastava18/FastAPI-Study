from typing import Annotated
from pydantic_core import PydanticCustomError
from pydantic import EmailStr

from fastapi import (Depends,
                     HTTPException, 
                     status, 
                     APIRouter,
                     Form)
from fastapi.security import OAuth2PasswordRequestForm

from utils.auth_utils import (get_password_hash,
                              Token, 
                              authenticate_user,
                              create_access_token,
                              oauth2_scheme,
                              validate_password_strength)

from dependencies import SessionDep
from database.database import  User
from config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

"""New user creation after validating the inputs"""
@router.post("/create-user/")
async def create_user(
    session: SessionDep,
    username: str = Form(...),
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
) -> User:
    # Check uniqueness of Username and Password
    if session.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if session.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Validate password strength
    validate_password_strength(password)

    # ✅ Validate email using Pydantic EmailStr
    try:
        EmailStr._validate(email)
    except PydanticCustomError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format. Please enter a valid email like name@example.com"
        )

    hashed_password = get_password_hash(password)
    new_user = User(username=username, full_name=fullname, email=email, hashed_password= hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

"""Create and return token after validation"""
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
async def secure_endpoint(
    token: str = Depends(oauth2_scheme)
    ):
    return {"token": token}
