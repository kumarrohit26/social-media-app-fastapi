from app import schemas
from app.config import settings
import pytest
from jose import jwt

# def test_root(client):
#     res = client.get('/')
#     assert res.json().get('message') == 'Hello, world'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={'email':'test@example.com', 'password': 'password123'})
    new_user = schemas.UserOut(**res.json())
    # check if we received the expected object
    assert new_user.email == 'test@example.com'
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login', data={'username':test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get('user_id')
    
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('username, password, status_code',[
    ('wrongemail@gmail.com', 'password123', 403),
    ('test@example.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test@example.com', None, 422),
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post('/login', data={'username':username, 'password': password})
    #assert res.json().get('detail') == 'Invalid Credentials'
    assert res.status_code == status_code
