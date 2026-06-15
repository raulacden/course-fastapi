from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'codingwithrobytest@example.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'
    
def test_change_password_success(test_user):
    response = client.put("/users/me/change-password", json={"password": "testpassword", "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert bcrypt_context.verify("newtestpassword", test_user.hashed_password)
    assert not bcrypt_context.verify("testpassword", test_user.hashed_password)
    
def test_change_password_invalid_password(test_user):
    response = client.put("/users/me/change-password", json={"password": "invalidpassword", "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid password"}
    assert bcrypt_context.verify("testpassword", test_user.hashed_password)
    
def test_change_phone_number_success(test_user):
    response = client.put("/users/me/change-phone-number", params={"phone_number": "(222)-222-2222"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert test_user.phone_number == "(222)-222-2222"