import typing

from apistar import annotate, http, exceptions, Response
from apistar.interfaces import Auth
from apistar.backends.django_orm import Session
from apistar_jwt.token import JWT
from django.conf import settings
from .models import Account, Envelope, Category, Transaction
from .schemas import AccountSchema, EnvelopeSchema, CategorySchema, TransactionSchema


def list_accounts(request: http.Request, auth: Auth, session: Session):
    queryset = session.Account.objects.filter(owner=auth.user['id'])
    return [AccountSchema(account) for account in queryset]


def create_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema):
    data['owner_id'] = data.pop('owner', None)
    account = session.Account.objects.create(**data)
    return Response(AccountSchema(account), status=201)
