from sqlmodel import SQLModel
from app.db.session import engine
from app.models.person import Person  # make sure all models are imported


def init_db():
    SQLModel.metadata.create_all(engine)
