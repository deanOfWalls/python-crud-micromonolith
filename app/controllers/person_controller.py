from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.models.person import Person, PersonCreate
from app.db.session import get_session
from app.repositories.person_repository import PersonRepository
from app.interfaces.person_service import PersonService  # Logic lives here
from app.services.person_service import PersonServiceDecorator  # Decorator layer

router = APIRouter(prefix="/person", tags=["Person"])


# Dependency injector
def get_person_service(session: Session = Depends(get_session)) -> PersonServiceDecorator:
    repo = PersonRepository(session)
    base_service = PersonService(repo)
    return PersonServiceDecorator(base_service)


@router.post("/", response_model=Person)
def create_person(
    person: PersonCreate,
    service: PersonServiceDecorator = Depends(get_person_service)
):
    return service.create(Person(**person.dict()))


@router.get("/{person_id}", response_model=Person)
def read_by_id(
    person_id: int,
    service: PersonServiceDecorator = Depends(get_person_service)
):
    person = service.read_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.get("/", response_model=List[Person])
def read_all(service: PersonServiceDecorator = Depends(get_person_service)):
    return service.read_all()


@router.put("/{person_id}", response_model=Person)
def update_person(
    person_id: int,
    data: Person,
    service: PersonServiceDecorator = Depends(get_person_service)
):
    updated = service.update(person_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated


@router.delete("/{person_id}", response_model=Person)
def delete_person(
    person_id: int,
    service: PersonServiceDecorator = Depends(get_person_service)
):
    deleted = service.delete(person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    return deleted
