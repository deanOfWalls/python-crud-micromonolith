from typing import List, Optional
from app.models.person import Person
from app.repositories.person_repository import PersonRepository
from datetime import date

class PersonServiceMixin:
    repository: PersonRepository  # will be injected

    def create(self, person: Person) -> Person:
        return self.repository.save(person)

    def read_by_id(self, person_id: int) -> Optional[Person]:
        return self.repository.find_by_id(person_id)

    def read_all(self) -> List[Person]:
        return self.repository.find_all()

    def update(self, person_id: int, data: Person) -> Optional[Person]:
        person = self.repository.find_by_id(person_id)
        if not person:
            return None
        person.first_name = data.first_name
        person.last_name = data.last_name
        person.birth_date = data.birth_date
        if isinstance(person.birth_date, str):
            person.birth_date = date.fromisoformat(person.birth_date)
        return self.repository.save(person)

    def delete(self, person_id: int) -> Optional[Person]:
        person = self.repository.find_by_id(person_id)
        if not person:
            return None
        self.repository.delete(person)
        return person
