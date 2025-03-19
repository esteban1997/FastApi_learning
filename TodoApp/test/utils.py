from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..models.models import Todos,Users
from ..routes.users import bcrypt_context

DATABASE_URL = "sqlite:///./testdb.db" 

engine = create_engine(
  DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
    
def override_get_current_user():
  return {'username':'es','id':1,'user_role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
  todo=Todos(
    title="Learn to code!",
    descripcion="neet to learn every day",
    priority=5,
    complete=False,
    owner_id=1,
  )
  
  db = TestingSessionLocal()
  db.add(todo)
  db.commit()
  yield todo
  with engine.connect() as connection:
    connection.execute(text("DELETE FROM todos;"))
    connection.commit()
    
@pytest.fixture
def test_user():
  user = Users(
    username="es",
    email="e@mail",
    first_name="Esteban",
    last_name="Aguirre",
    hashed_password=bcrypt_context.hash("test"),
    role="admin",
    phone_number="11223344"
  )
  
  db=TestingSessionLocal()
  db.add(user)
  db.commit()
  yield user
  with engine.connect() as connection:
    connection.execute(text("Delete FROM users;"))
    connection.commit()