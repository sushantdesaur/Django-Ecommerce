from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial="IN"),
        }
        