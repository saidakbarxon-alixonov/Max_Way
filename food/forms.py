from django import forms
from .models import Customer, Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "phone_number"]


class OrderForm(forms.ModelForm):
    # Only these two values are accepted (1 = cash, 2 = terminal).
    payment_type = forms.TypedChoiceField(
        choices=[(1, "Cash"), (2, "Terminal")],
        coerce=int,
    )

    class Meta:
        model = Order
        # `status` and `customer` are set by the server, never by the browser.
        fields = ["payment_type", "address"]
