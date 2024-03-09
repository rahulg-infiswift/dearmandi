from fastapi import FastAPI
import uvicorn
from python_accounting.config import config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select

from python_accounting.models import Base
from sqlalchemy import create_engine
from python_accounting.database.session import get_session
from python_accounting.models import Entity, Currency

# url = "postgresql://postgres:ashoktraders@localhost:5432/dearmandi-dev"
# config = config.Config("api/config.toml")
database = config.database
engine = create_engine(database["url"])

app = FastAPI()
Base.metadata.create_all(engine) # run migrations to create tables

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api/list_entities")
def list_entities():
    with get_session(engine) as session:
        stmt = select(Entity)
        entities = session.scalars(stmt).all()
        return entities


@app.get("/api/create_entity/{name}")
def create_entity(name: str):
    print("Hello there!")
    with get_session(engine) as session:
        entity = Entity(name=name)
        session.add(entity)
        session.commit() # This automatically sets up a Reporting Period for the Entity

        currency = Currency(name="US Dollars", code="USD", entity_id=entity.id)
        session.add(currency)
        session.commit()

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
