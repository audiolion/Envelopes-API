import typing

from apistar import annotate, http, exceptions, Response
from apistar.interfaces import Auth
from apistar.backends.django_orm import Session
from apistar_jwt.token import JWT
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Account, Envelope, Category, Transaction
from .schemas import AccountSchema, EnvelopeSchema, CategorySchema, TransactionSchema


def retrieve(queryset):
    try:
        if queryset.exists():
            return {'obj': queryset.get(), 'success': True, 'exception': None}
    except ObjectDoesNotExist as e:
        return {'obj': None, 'success': False, 'exception': e}
    except Exception as f:
        return {'obj': None, 'success': False, 'exception': e}
    return {'obj': queryset, 'success': False, 'exception': None}


def list_accounts(request: http.Request, auth: Auth, session: Session):
    queryset = session.Account.objects.filter(owner=auth.user['id'])
    return [AccountSchema(account) for account in queryset]


def get_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['success']:
        return AccountSchema(props['obj'])
    elif props['exception']:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)


def create_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema):
    data['owner_id'] = data.pop('owner', None)
    account = session.Account.objects.create(**data)
    return Response(AccountSchema(account), status=201)


def update_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['success']:
        for attr, value in data.items():
            setattr(props['obj'], attr, value)
        props['obj'].save()
        return AccountSchema(account)
    elif props['exception']:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)


def delete_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['success']:
        props['obj'].delete()
        return Response(None, status=204)
    elif props['exception']:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)
