import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from config.settings import settings
import django

django.setup()

from apistar import Component, Include, Route
from apistar.backends import django_orm
from apistar.frameworks.wsgi import WSGIApp as App
from apistar_jwt.authentication import get_jwt
from apistar_jwt.token import JWT

from envelopes import views


account_routes = [
    Route('/', 'GET', views.list_accounts),
    Route('/', 'POST', views.create_account),
    Route('/{uuid}/', 'GET', views.get_account),
    Route('/{uuid}/', 'PATCH', views.update_account),
    Route('/{uuid}/', 'DELETE', views.delete_account),
]

envelope_routes = [
    # Route('/', 'GET', list_envelopes),
    # Route('/', 'POST', create_envelope),
    # Route('/{uuid}', 'GET', get_envelope),
    # Route('/{uuid}', 'PUT', update_envelope),
    # Route('/{uuid}', 'PATCH', update_envelope),
    # Route('/{uuid}', 'DELETE', delete_envelope),
    # Route('/{uuid}/deposit', 'POST', deposit_into_envelope),
    # Route('/{uuid}/withdraw', 'POST', withdraw_from_envelope),
]

routes = [
   Include('/accounts', account_routes),
   # Include('/envelope', envelope_rtoues),
]


components = [
    Component(JWT, init=get_jwt)
]

components = components + django_orm.components

app = App(
    routes=routes,
    components=components,
    settings=settings,
    commands=django_orm.commands,  # Install custom commands.
)
