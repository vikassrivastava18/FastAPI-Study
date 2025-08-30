"""
    This module sets up the database connection and ORM models for a FastAPI application using SQLModel and SQLite.
    - Defines the SQLite database file and connection URL.
    - Configures connection arguments to allow multi-threaded access, suitable for web applications.
    - Initializes the SQLModel engine for database operations.
    - Declares two ORM models:
        - User: Represents application users with fields for username, full name, email, hashed password, and disabled status.
        - Hero: Represents hero entities with fields for name, age, and secret name.
    - Provides utility functions:
        - create_db_and_tables: Creates database tables based on defined models.
        - get_session: Dependency function to yield a database session for use in FastAPI routes.
"""

from sqlmodel import (
    create_engine,
    SQLModel,
    Session,
    Field)

"""
Define the database path
"""
sqlitie_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlitie_file_name}"

"""
allows the SQLite connection to be shared across multiple threads, 
which is required for web apps like FastAPI to avoid threading errors.
"""
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str = Field()
    email: str | None = Field(unique=True)
    hashed_password: str = Field()
    disabled: bool = Field(default=False)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session