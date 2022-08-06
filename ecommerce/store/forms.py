import email
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import ShippingAddress, Customer

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address', 'landmark', 'city',
                  'state', 'zipcode', 'phone_number')
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial="IN"),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'email')