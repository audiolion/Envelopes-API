# Standard Library Imports
import json
import uuid
from itertools import chain

# Third Party Library Imports
from behaviors.behaviors import Timestamped
from django.conf import settings
from django.db import transaction as db_transaction
from django.db import models

# Local Imports
from .utils import encode


class JsonModelMixin:
    def to_dict(self, include=None, exclude=None):
        data = {}
        include = set(self._meta.get_fields()) if include is None else set(include)
        exclude = set() if exclude is None else set(exclude)
        include -= exclude
        opts = self._meta
        for field in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if field in include:
                data[field.name] = field.value_from_object(self)
                if field.many_to_many:
                    if instance.pk is None:
                        data[field.name] = []
                    else:
                        data[field.name] = list(field.value_from_object(instance).values_list('pk', flat=True))
                # data.update({field.name: getattr(self, field.name, None)})
                # TODO: handle relations to output their serializable value (primary key??)
        return data

    def to_json(self, include=None, exclude=None):
        return json.dumps(self.to_dict(include, exclude))


class Account(JsonModelMixin, Timestamped):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)


class Envelope(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Envelope Identifier')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text='User who created the envelope.',
        related_name='envelopes',
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2)
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    account = models.ForeignKey(Account, related_name='envelopes')
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    @classmethod
    def create(cls, user, dt, account, **kwargs):
        # get budget, default to 0
        budget = kwargs.get('budget', 0)
        # if balance not exist, default to initial budget amount
        balance = kwargs.get('balance', budget)
        with db_transaction.atomic():
            envelope = cls.objects.create(
                creator=user,
                created=dt,
                modified=dt,
                account=account,
                budget=budget,
                balance=balance,
                **kwargs,
            )
            transaction = Transaction.create(
                user=user,
                envelope=envelope,
                type=Transaction.ACTION_TYPE_CREATED,
                delta=0,
                created=dt,
            )
        return envelope, transaction

    @classmethod
    def deposit(cls, uuid, deposited_by, amount, dt, description=None, comment=None):
        assert amount > 0
        description = '' if description is None else description
        comment = '' if comment is None else comment
        with db_transaction.atomic():
            envelope = cls.objects.select_for_update().get(uuid=uuid)
            envelope.balance += amount
            envelope.modified = dt
            envelope.save(update_fields=[
                'balance',
                'modified',
            ])
            transaction = Transaction.create(
                user=deposited_by,
                envelope=envelope,
                type=Transaction.ACTION_TYPE_DEPOSITED,
                delta=amount,
                created=dt,
                description=description,
                comment=comment,
            )
        return envelope, transaction

    @classmethod
    def withdraw(cls, uuid, withdrawn_by, amount, dt, description=None, comment=None):
        assert amount > 0
        description = '' if description is None else description
        comment = '' if comment is None else comment
        with transaction.atomic():
            envelope = cls.objects.select_for_update().get(uuid=uuid)
            envelope.balance -= amount
            envelope.modified = dt
            envelope.save(update_fields=[
                'balance',
                'modified',
            ])
            transaction = Transaction.create(
                user=withdrawn_by,
                envelope=envelope,
                type=Transaction.ACTION_TYPE_WITHDRAWN,
                delta=-amount,
                created=dt,
                description=description,
                comment=comment,
            )
        return envelope, transaction


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)


class Transaction(models.Model):
    ACTION_TYPE_CREATED = 'CREATED'
    ACTION_TYPE_DEPOSITED = 'DEPOSITED'
    ACTION_TYPE_WITHDRAWN = 'WITHDRAWN'
    ACTION_TYPE_CHOICES = (
        (ACTION_TYPE_CREATED, 'Created'),
        (ACTION_TYPE_DEPOSITED, 'Deposited'),
        (ACTION_TYPE_WITHDRAWN, 'Withdrawn'),
    )

    id = models.AutoField(primary_key=True)
    friendly_id = models.CharField(max_length=30, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text='User who performed the action.',
        related_name='transactions',
    )
    created = models.DateTimeField(blank=True)
    envelope = models.ForeignKey(Envelope, related_name='transactions')
    type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    delta = models.DecimalField(max_digits=14, decimal_places=2, help_text="Balance delta")
    description = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, related_name='transactions')
    comment = models.TextField(blank=True)

    @classmethod
    def create(cls, user, envelope, type, delta, dt, description=None, comment=None, **kwargs):
        assert dt is not None
        description = '' if description is None else description
        comment = '' if comment is None else comment
        friendly_id = encode(dt.timestamp(), delta, envelope.pk, user.pk)
        return cls.objects.create(
            friendly_id=friendly_id,
            created=dt,
            user=user,
            envelope=envelope,
            type=type,
            delta=delta,
            description=description,
            comment=comment,
            **kwargs
        )
