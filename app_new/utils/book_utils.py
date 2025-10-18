from pydantic import BaseModel


# Books structure definition
class BookRegister(BaseModel):
    name: str