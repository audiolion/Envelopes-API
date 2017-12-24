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


def get_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    try:
        if queryset.exists():
            return AccountSchema(queryset.get())
    except Exception:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)


def create_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema):
    data['owner_id'] = data.pop('owner', None)
    account = session.Account.objects.create(**data)
    return Response(AccountSchema(account), status=201)


def update_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    try:
        if queryset.exists():
            account = queryset.get()
            for attr, value in data.items():
                setattr(account, attr, value)
            account.save()
            return AccountSchema(account)
    except Exception:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)
