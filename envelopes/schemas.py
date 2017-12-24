from apistar import typesystem

from .models import Transaction


class AccountSchema(typesystem.Object):
    properties = {
        'id': typesystem.integer(minimum=1),
        'uuid': typesystem.string(min_length=36),
        'balance': typesystem.number(),
        'owner_id': typesystem.integer(minimum=1),
        'created': typesystem.string(format='date'),
        'modified': typesystem.string(format='date'),
    }


class CategorySchema(typesystem.Object):
    properties = {
        'name': typesystem.string(min_length=1, max_length=80),
    }


class EnvelopeSchema(typesystem.Object):
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
        Transaction.ACTION_TYPE_CREATED,
        Transaction.ACTION_TYPE_DEPOSITED,
        Transaction.ACTION_TYPE_WITHDRAWN,
    ]


class TransactionSchema(typesystem.Object):
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
