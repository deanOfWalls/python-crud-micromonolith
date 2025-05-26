✅ The 3 Statements for Doing Python Right (Inspired by Java Best Practices)
All method implementations go in a mixin.
➤ This keeps logic out of interfaces and avoids inheritance bloat in concretes.

Abstracts wire state, concretes wire values.
➤ Abstract base classes may wire shared **init** state (rare); concretes assemble dependencies via constructors.

Interfaces define contracts, mixins define behavior.
➤ abc.ABC declares what must exist; mixins declare how it behaves.

# Python CRUD Monolith Walkthrough

This guide walks through building a layered Python CRUD app using **FastAPI**, **SQLModel**, and a clean Java-style architecture. The app includes a minimal vanilla JavaScript front-end.

---

## 📁 Project Structure

```
app/
├── config/
│   └── database.py           # DB schema init (SQLModel.create_all)
├── controllers/
│   └── person_controller.py  # FastAPI routes
├── db/
│   ├── session.py            # engine + get_session
│   └── init_db.py            # (unused) alternate init
├── interfaces/
│   └── person_service.py     # contract (Protocol)
├── mixins/
│   └── person_service_mixin.py  # behavior logic
├── models/
│   └── person.py             # SQLModel: Person, PersonCreate
├── repositories/
│   └── person_repository.py  # DB queries
├── services/
│   └── person_service.py     # PersonServiceImpl wiring
├── static/
│   ├── index.html
│   ├── service.js
│   └── style.css
├── main.py                   # App entrypoint
```

---

## 🧠 Key Backend Design Choices

* Clean OOP architecture using `interface + mixin + concrete` layering
* **SQLModel** for typed models, validation, and SQLite ORM
* **FastAPI** for web routing + DI
* Manual dependency injection
* Single responsibility per file
* Static analysis ready (type hints + mypy)

---

## Front-End (Static)

### 📄 `index.html`

```html
<!-- See full file in app/static/index.html -->
<!-- HTML form and list bound to JS with jQuery -->
```

### 📜 `service.js`

```js
// AJAX handlers for submitting and loading people
```

### 🎨 `style.css`

```css
/* Simple responsive design with padding, shadow, spacing */
```

---

## Backend Components (Code Examples)

### ✅ `models/person.py`

```python
class PersonBase(SQLModel):
    first_name: str
    last_name: str
    birth_date: date

class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PersonCreate(PersonBase):
    pass
```

### ✅ `db/session.py`

```python
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

### ✅ `config/database.py`

```python
from sqlmodel import SQLModel
from app.db.session import engine
from app.models.person import Person

def init_db():
    SQLModel.metadata.create_all(engine)
```

### ✅ `interfaces/person_service.py`

```python
class PersonService(Protocol):
    def create(self, person: Person) -> Person: ...
    def read_by_id(self, person_id: int) -> Optional[Person]: ...
    def read_all(self) -> List[Person]: ...
    def update(self, person_id: int, data: Person) -> Optional[Person]: ...
    def delete(self, person_id: int) -> Optional[Person]: ...
```

### ✅ `mixins/person_service_mixin.py`

```python
from datetime import date

class PersonServiceMixin:
    repository: PersonRepository

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
        person.birth_date = date.fromisoformat(str(data.birth_date))
        return self.repository.save(person)

    def delete(self, person_id: int) -> Optional[Person]:
        person = self.repository.find_by_id(person_id)
        if not person:
            return None
        self.repository.delete(person)
        return person
```

### ✅ `services/person_service.py`

```python
class PersonServiceImpl(PersonServiceMixin):
    def __init__(self, repository: PersonRepository):
        self.repository = repository
```

### ✅ `repositories/person_repository.py`

```python
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
```

### ✅ `controllers/person_controller.py`

```python
@router.post("/", response_model=Person)
def create_person(...): ...

@router.get("/{person_id}", response_model=Person)
def read_by_id(...): ...

@router.get("/", response_model=List[Person])
def read_all(...): ...

@router.put("/{person_id}", response_model=Person)
def update_person(...): ...

@router.delete("/{person_id}", response_model=Person)
def delete_person(...): ...
```

### ✅ `main.py`

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config.database import init_db
from app.controllers.person_controller import router as person_router

static_path = "app/static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(person_router)

if os.path.exists(os.path.join(static_path, "index.html")):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
```

---

✅ Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the UI
✅ Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger docs

You're done.
