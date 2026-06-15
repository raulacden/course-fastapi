from datetime import timedelta

from .utils import *
from routers.auth import create_access_token, get_current_user, get_db, authenticated_user, SECRET_KEY, ALGORITHM
from jose import jwt
import pytest
from fastapi import HTTPException, status

app.dependency_overrides[get_db] = override_get_db

def test_authenticated_user(test_user):
    db = TestingSessionLocal()
    user = authenticated_user(db, test_user.username, 'testpassword')
    assert user is not None
    assert user.username == test_user.username
    assert user.email == test_user.email
    assert user.first_name == test_user.first_name
    assert user.last_name == test_user.last_name
    assert user.role == test_user.role
    assert user.phone_number == test_user.phone_number
    
    non_existent_user = authenticated_user(db, "wrongusername", "testpassword")
    assert non_existent_user is False
    
    wrong_password_user = authenticated_user(db, test_user.username, "wrongpassword")
    assert wrong_password_user is False
    
def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(minutes=15)
    
    token = create_access_token(username, user_id, role, expires_delta)
    
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}
    
@pytest.mark.asyncio
async def test_get_current_user_missing_pyload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"