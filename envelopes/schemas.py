# Third Party Library Imports
from marshmallow import Schema, ValidationError, fields, post_load, validate

# Local Imports
from . import models


class Account(Schema):
    id = fields.Integer(min=1)
    uuid = fields.UUID()
    balance = fields.Decimal(places=2, required=True, as_string=True)
    owner_id = fields.Integer(min=1, required=True, load_from='owner', dump_to='owner')
    created = fields.DateTime()
    modified = fields.DateTime(allow_none=True)

    @post_load
    def make_account(self, data):
        return self.context['session'].Account(**data)


class Envelope(Schema):
    id = fields.Integer(min=1)
    uuid = fields.UUID()
    budget = fields.Decimal(places=2, required=True, as_string=True)
    balance = fields.Decimal(places=2, required=True, as_string=True)
    creator_id = fields.Integer(min=1, required=True, load_from='creator', dump_to='creator')
    name = fields.String(validate=[validate.Length(max=50)])
    description = fields.String(validate=[validate.Length(max=200)])
    account_id = fields.Integer(min=1, required=True, load_from='account', dump_to='account')
    created = fields.DateTime()
    modified = fields.DateTime(allow_none=True)

    @post_load
    def make_envelope(self, data):
        return self.context['session'].Envelope(**data)


class Category(Schema):
    id = fields.Integer(min=1)
    name = fields.String(validate=[validate.Length(max=80)])

    @post_load
    def make_category(self, data):
        return self.context['session'].Category(**data)


ACTION_TYPES = [action_type for (action_type, _) in models.Transaction.ACTION_TYPE_CHOICES]


def must_be_action_type(data):
    if data not in ACTION_TYPES:
        raise ValidationError('Data must be one of "{}"'.format(ACTION_TYPES))


class Transaction(Schema):
    id = fields.Integer(min=1)
    friendly_id = fields.String(validate=[validate.Length(max=30)], dump_only=True)
    user_id = fields.Integer(min=1, required=True, load_from='user', dump_to='user')
    created = fields.DateTime()
    envelope_id = fields.Integer(min=1, required=True, load_from='envelope', dump_to='envelope')
    action_type = fields.String(validate=[must_be_action_type])
    delta = fields.Decimal(places=2, required=True, as_string=True)
    description = fields.String(validate=[validate.Length(max=100)])
    category_id = fields.Integer(min=1, required=True, load_from='category', dump_to='category')
    comment = fields.String()
