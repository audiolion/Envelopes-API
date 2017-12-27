# Third Party Library Imports
from marshmallow import Schema, fields, post_load


class Account(Schema):
    id = fields.Integer(min=1)
    uuid = fields.UUID()
    balance = fields.Decimal(places=2, required=True, as_string=True)
    owner_id = fields.Integer(min=1, required=True, load_from='owner', dump_to='owner')
    created = fields.DateTime()
    modified = fields.DateTime()

    @post_load
    def make_account(self, data):
        return self.context['session'].Account(**data)
