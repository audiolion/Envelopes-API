# Third Party Library Imports
from marshmallow import Schema, fields, post_load, validate


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
