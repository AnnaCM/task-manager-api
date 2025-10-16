import pytest
from database import get_db
from datetime import datetime
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from models import Base, Tasks
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def create_test_db():
    Base.metadata.create_all(bind=engine)


def drop_test_db():
    Base.metadata.drop_all(bind=engine)


def populate_test_data(db: Session):
    created_at_1 = int(datetime(2023, 1, 1, 12, 0).timestamp())
    updated_at_1 = None

    created_at_2 = int(datetime(2023, 1, 2, 10, 0).timestamp())
    updated_at_2 = int(datetime(2023, 1, 2, 18, 0).timestamp())

    db.add_all([
        Tasks(id=1, title="Test Task 1", completed=False, created_at=created_at_1, updated_at=updated_at_1),
        Tasks(id=2, title="Test Task 2", completed=True, created_at=created_at_2, updated_at=updated_at_2),
    ])
    db.commit()


@pytest.fixture(scope="module")
def test_db():
    create_test_db()

    db = TestingSessionLocal()
    populate_test_data(db)
    yield db

    drop_test_db()
    db.close()
