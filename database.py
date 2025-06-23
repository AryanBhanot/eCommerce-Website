from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Yields a database session."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Creates all database tables."""
    SQLModel.metadata.create_all(engine)
