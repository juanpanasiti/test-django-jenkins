from django import forms


class CreditCardForm(forms.Form):
    name = forms.CharField(max_length=50,min_length=1)
    limit_amount = forms.IntegerField(min_value=0)
    last_close_date = forms.DateField()
    last_exp_date = forms.DateField()
    current_close_date = forms.DateField()
    current_exp_date = forms.DateField()
    next_close_date = forms.DateField()
    next_exp_date = forms.DateField()