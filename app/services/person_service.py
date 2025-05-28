from typing import List, Optional
from app.models.person import Person
from app.interfaces.person_service import PersonService


class PersonServiceImpl:
    def __init__(self, delegate: PersonService):
        self.delegate = delegate

    def create(self, person: Person) -> Person:
        return self.delegate.create(person)

    def read_by_id(self, person_id: int) -> Optional[Person]:
        return self.delegate.read_by_id(person_id)

    def read_all(self) -> List[Person]:
        return self.delegate.read_all()

    def update(self, person_id: int, data: Person) -> Optional[Person]:
        return self.delegate.update(person_id, data)

    def delete(self, person_id: int) -> Optional[Person]:
        return self.delegate.delete(person_id)
