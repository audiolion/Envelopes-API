# Third Party Library Imports
from apistar import Response, http
from apistar.backends.django_orm import Session
from apistar.interfaces import Auth
from django.core.exceptions import ObjectDoesNotExist

# Local Imports
from .schemas import AccountSchema


def retrieve(queryset):
    try:
        if queryset.exists():
            return {'obj': queryset.get(), 'success': True, 'exception': None}
    except ObjectDoesNotExist as e:
        return {'obj': None, 'success': False, 'exception': e}
    except Exception as f:
        return {'obj': None, 'success': False, 'exception': f}
    return {'obj': queryset, 'success': False, 'exception': None}


def handle_error(props):
    if props['exception']:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)


def list_accounts(request: http.Request, auth: Auth, session: Session):
    queryset = session.Account.objects.filter(owner=auth.user['id'])
    return [AccountSchema(account) for account in queryset]


def get_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    return AccountSchema(props['obj'])


def create_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema):
    account = session.Account.objects.create(**data)
    return Response(AccountSchema(account), status=201)


def update_account(request: http.Request, auth: Auth, session: Session, data: AccountSchema, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    for attr, value in data.items():
        setattr(props['obj'], attr, value)
    props['obj'].save()
    return AccountSchema(props['obj'])


def delete_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    props['obj'].delete()
    return Response(None, status=204)
