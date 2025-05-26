from sqlmodel import SQLModel
from app.db.session import engine
from app.models.person import Person  # ensures model is loaded

def init_db():
    SQLModel.metadata.create_all(bind=engine)
