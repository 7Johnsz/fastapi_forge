
from sqlmodel import SQLModel, Session, create_engine, select
from loguru import logger

import os

class Database:
    def __init__(self) -> None:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
                
        try:
            self.engine = create_engine(connection_string, echo=True)
            self.engine.connect()
            logger.info("Database connection established.")

        except Exception as e:
            raise RuntimeError(f"Database connection failed: {e}")

    def query(self, model, where_clause=None):
        with Session(self.engine) as session:
            stmt = select(model)
            if where_clause:
                stmt = stmt.where(where_clause)
            return session.exec(stmt).all()

    def add(self, instance: SQLModel):
        with Session(self.engine) as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance

db = Database()

def get_session():
    with Session(db.engine) as session:
        yield session