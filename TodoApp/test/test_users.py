from .utils import *
from ..routes.users import get_db,get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
  response = client.get("/user")
  assert response.status_code == status.HTTP_200_OK
  assert response.json()['username'] == 'es'
  assert response.json()['email'] == 'e@mail'
  assert response.json()['first_name'] == 'Esteban'
  assert response.json()['last_name'] == 'Aguirre'
  assert response.json()['role'] == 'admin'
  assert response.json()['phone_number'] == '11223344'
  
def test_change_password_success(test_user):
  response = client.put("/user/change_password",params={"old_password":"test","new_password":"nueva"})
  assert response.status_code == status.HTTP_204_NO_CONTENT
  
def test_change_password_invalid(test_user):
  response = client.put("/user/change_password",params={"old_password":"test2","new_password":"nueva"})
  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {'detail':'Incorrect password'}
  

def test_change_phone_success(test_user):
  response = client.put("/user/phonenumber/123123123")
  assert response.status_code == status.HTTP_204_NO_CONTENT