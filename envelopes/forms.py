# Third Party Library Imports
from django import forms

# Local Imports
from .models import Account, Category, Envelope


class AccountForm(forms.ModelForm):
    balance = forms.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = Account
        fields = ('balance', 'owner')


class EnvelopeForm(forms.ModelForm):
    balance = forms.DecimalField(max_digits=14, decimal_places=2)
    budget = forms.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = Envelope
        fields = ('name', 'description', 'budget', 'balance', 'account')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', )
