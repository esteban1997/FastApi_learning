
from ..routes.todos import get_current_user,get_db
from fastapi import status
from ..models.models import Todos
from .utils import *

    
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
  response = client.get("/todos")
  assert response.status_code==status.HTTP_200_OK
  assert response.json()==[{'complete':False,'title':'Learn to code!',
                            'descripcion':"neet to learn every day",
                            'priority':5,'owner_id':1,'id':1}]
  

def test_read_one_authenticated(test_todo):
  response = client.get("/todos/todo/1")
  assert response.status_code==status.HTTP_200_OK
  assert response.json()=={'complete':False,'title':'Learn to code!',
                            'descripcion':"neet to learn every day",
                            'priority':5,'owner_id':1,'id':1}
  
  
def test_read_one_authenticated_not_found(test_todo):
  response = client.get("/todos/todo/999")
  assert response.status_code==status.HTTP_404_NOT_FOUND
  assert response.json()=={'detail':'todo not found.'}
  
def test_create_todo(test_todo):
  request_data={
    'title':'new todo',
    'descripcion':'new todo',
    'priority':5,
    'complete':False
  }
  
  response=client.post('/todos/todo/',json=request_data)
  assert response.status_code == 201
  
  db = TestingSessionLocal()
  model = db.query(Todos).filter(Todos.id==2).first()
  assert model.title==request_data.get('title')
  assert model.descripcion==request_data.get('descripcion')
  assert model.priority==request_data.get('priority')
  assert model.complete==request_data.get('complete')