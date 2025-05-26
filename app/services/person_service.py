from app.models.person import Person
from app.interfaces.person_service import PersonService
from app.mixins.person_service_mixin import PersonServiceMixin
from app.repositories.person_repository import PersonRepository


class PersonServiceImpl(PersonServiceMixin):
    def __init__(self, repository: PersonRepository):
        self.repository = repository
