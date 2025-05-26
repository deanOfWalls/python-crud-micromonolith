from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class PersonBase(SQLModel):
    first_name: str
    last_name: str
    birth_date: date

class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PersonCreate(PersonBase):
    pass
