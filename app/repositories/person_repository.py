from sqlmodel import Session, select
from app.models.person import Person
from typing import List, Optional

class PersonRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, person: Person) -> Person:
        self.session.add(person)
        self.session.commit()
        self.session.refresh(person)
        return person

    def find_by_id(self, person_id: int) -> Optional[Person]:
        return self.session.get(Person, person_id)

    def find_all(self) -> List[Person]:
        statement = select(Person)
        return list(self.session.exec(statement))

    def delete(self, person: Person) -> None:
        self.session.delete(person)
        self.session.commit()
