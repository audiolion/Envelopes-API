import os

import pytest

from apistar import Settings, TestClient
from apistar_jwt.token import JWT
from django.contrib.auth import get_user_model

from envelopes.models import Account
from app import app


User = get_user_model()

def create_auth(user):
    payload = {'user': user.id, 'username': user.email}
    jwt = JWT.encode(
        payload, os.environ.get('JWT_SECRET'), algorithm='HS256')
    auth_header = {
        'Authorization': 'Bearer {}'.format(jwt)
    }
    return {'user': user, 'jwt': jwt, 'header': auth_header}


@pytest.fixture()
def auth():
    user, _ = User.objects.get_or_create(
        email='test@example.com',
        password='12345abc',
    )
    return create_auth(user)


@pytest.fixture()
def accounts():
    emails = [
        '1-test@example.com',
        '2-test@example.com',
        '3-test@example.com',
    ]
    users = []
    for email in emails:
        user, _ = User.objects.get_or_create(
            email=email,
            password='12345abc',
        )
        users.append(user)
    accounts = []
    for u in users:
        account, _ = Account.objects.get_or_create(
            balance=100,
            owner=u,
        )
        accounts.append(account)
    return accounts


def test_list_accounts(auth, accounts):
    client = TestClient(app)
    res = client.get('/accounts/', headers=auth['header'])
    assert res.status_code == 200
    assert res.json() == []

    auth = create_auth(accounts[0].owner)
    res = client.get('/accounts/', headers=auth['header'])
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]['uuid'] == str(accounts[0].uuid)

    res = client.get('/accounts/')
    assert res.status_code == 401
