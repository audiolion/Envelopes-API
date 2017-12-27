# Third Party Library Imports
from django import forms

# Local Imports
from .models import Account


class AccountForm(forms.ModelForm):
    balance = forms.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = Account
        fields = ('balance', 'owner')
