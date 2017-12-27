# Third Party Library Imports
from apistar import typesystem

# Local Imports
from . import models


class Account(typesystem.Object):
    properties = {
        'id': typesystem.integer(minimum=1),
        'uuid': typesystem.string(),
        'balance': typesystem.number(),
        'owner_id': typesystem.integer(minimum=1),
        'created': typesystem.string(),
        'modified': typesystem.string(),
    }


class Category(typesystem.Object):
    properties = {
        'name': typesystem.string(min_length=1, max_length=80),
    }


class Envelope(typesystem.Object):
    properties = {
        'id': typesystem.integer(minimum=1),
        'uuid': typesystem.string(min_length=36),
        'creator': typesystem.integer(minimum=1),
        'name': typesystem.string(min_length=1, max_length=50),
        'description': typesystem.string(max_length=200),
        'budget': typesystem.number(),
        'balance': typesystem.number(),
        'account': typesystem.integer(minimum=1),
        'created': typesystem.string(format='date'),
        'modified': typesystem.string(format='date'),
    }


class ActionTypeEnum(typesystem.Enum):
    enum = [
        models.Transaction.ACTION_TYPE_CREATED,
        models.Transaction.ACTION_TYPE_DEPOSITED,
        models.Transaction.ACTION_TYPE_WITHDRAWN,
    ]


class Transaction(typesystem.Object):
    properties = {
        'id': typesystem.integer(minimum=1),
        'friendly_id': typesystem.string(max_length=30),
        'user': typesystem.integer(minimum=1),
        'created': typesystem.string(format="date"),
        'envelope': typesystem.integer(minimum=1),
        'type': ActionTypeEnum,
        'delta': typesystem.number(),
        'description': typesystem.string(max_length=100),
        'category': typesystem.integer(minimum=1),
        'comment': typesystem.string(),
    }
