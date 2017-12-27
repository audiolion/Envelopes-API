# Third Party Library Imports
from apistar import Response, http
from apistar.backends.django_orm import Session
from apistar.interfaces import Auth
from django.core.exceptions import ObjectDoesNotExist

# Local Imports
from . import schemas
from .forms import AccountForm

account_schema = schemas.Account(exclude=('id'))


def retrieve(queryset):
    try:
        if queryset.exists():
            return {'obj': queryset.get(), 'error': False, 'exception': None}
    except ObjectDoesNotExist as e:
        return {'obj': None, 'error': True, 'exception': e}
    except Exception as f:
        return {'obj': None, 'error': True, 'exception': f}
    return {'obj': queryset, 'error': True, 'exception': None}


def handle_error(props):
    if props['exception']:
        return Response({'message': 'Bad request'}, status=400)
    return Response({'message': 'Not found'}, status=404)


def list_accounts(request: http.Request, auth: Auth, session: Session):
    queryset = session.Account.objects.filter(owner=auth.user['id'])
    accounts = account_schema.dump(queryset, many=True)
    return accounts.data


def get_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    account, errors = account_schema.dump(props['obj'])
    if errors:
        return Response(errors, status=400)
    return account


def create_account(request: http.Request, auth: Auth, session: Session, data: http.RequestData):
    account_schema.context['session'] = session
    if hasattr(data, 'get') and not data.get('owner'):
        data['owner'] = auth.user['id']
    account, errors = account_schema.load(data)
    if errors:
        return Response(errors, status=400)
    account.save()
    return Response(account_schema.dump(account).data, status=201)


def update_account(request: http.Request, auth: Auth, session: Session, data: http.RequestData, uuid):  # noqa; E501
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    form = AccountForm(data, instance=props['obj'])
    if form.is_valid():
        account = form.save()
        return account_schema.dump(account).data
    return Response(form.errors, status=400)


def delete_account(request: http.Request, auth: Auth, session: Session, uuid):
    queryset = session.Account.objects.filter(uuid=uuid).filter(owner=auth.user['id'])
    props = retrieve(queryset)
    if props['error']:
        return handle_error(props)
    props['obj'].delete()
    return Response(None, status=204)
