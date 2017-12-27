# Standard Library Imports
import os

# Third Party Library Imports
import pytest
from apistar import TestClient
from apistar_jwt.token import JWT
from django.contrib.auth import get_user_model

# First Party Library Imports
from app import app
from envelopes.models import Account

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
    for item in res.json():
        assert item['owner'] == auth['user'].id

    auth = create_auth(accounts[0].owner)
    res = client.get('/accounts/', headers=auth['header'])
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]['uuid'] == str(accounts[0].uuid)

    res = client.get('/accounts/')
    assert res.status_code == 401


def test_get_account(auth, accounts):
    client = TestClient(app)
    url = '/accounts/{}/'.format(accounts[0].uuid)
    res = client.get(url, headers=auth['header'])
    assert res.status_code == 404
    assert res.json() == {'message': 'Not found'}

    auth = create_auth(accounts[0].owner)
    res = client.get(url, headers=auth['header'])
    assert res.status_code == 200
    assert res.json()['uuid'] == str(accounts[0].uuid)
    with pytest.raises(KeyError):
        res.json()['id']

    res = client.get(url)
    assert res.status_code == 401


def test_create_account(auth):
    client = TestClient(app)
    data = {
        'balance': '100.00',
        'owner': auth['user'].id
    }
    res = client.post('/accounts/', headers=auth['header'], data=data)
    assert res.status_code == 201
    assert res.json()['owner'] == data['owner']
    assert res.json()['balance'] == data['balance']
    Account.objects.get(id=res.json()['id']).delete()

    res = client.post('/accounts/', data=data)
    assert res.status_code == 401

    res = client.post('/accounts/', headers=auth['header'], data={'owner': data['owner']})
    assert res.status_code == 400

    # this test fails due to test client using an ImmutableDict and that being passed
    # see https://github.com/encode/apistar/issues/379 for resolution
    #
    # res = client.post('/accounts/', headers=auth['header'], data={'balance': 50.0})
    # assert res.status_code == 201
    # assert res.json()['owner'] == data['owner']
    # assert res.json()['balance'] == data['balance']
    # Account.objects.get(id=res.json()['id']).delete()


def test_update_account(accounts):
    client = TestClient(app)
    url = '/accounts/{}/'.format(accounts[0].uuid)
    auth = create_auth(accounts[0].owner)
    data = {'balance': accounts[0].balance + 1, 'owner': accounts[0].owner.id}
    res = client.patch(url, headers=auth['header'], data=data)
    assert res.status_code == 200
    assert float(res.json()['balance']) == float(accounts[0].balance) + 1
    uuid = res.json()['uuid']

    res = client.patch(url, {'balance': 500})
    assert res.status_code == 401

    res = client.patch(url, headers=auth['header'], data={'id': 500})
    assert res.status_code == 400

    account = Account.objects.get(uuid=uuid)
    account.balance = 100.00
    account.save()


def test_delete_account(accounts):
    client = TestClient(app)
    url = '/accounts/{}/'.format(accounts[0].uuid)
    auth = create_auth(accounts[0].owner)
    uuid = accounts[0].uuid
    res = client.delete(url, headers=auth['header'])
    assert res.status_code == 204
    assert not Account.objects.filter(uuid=uuid).exists()
