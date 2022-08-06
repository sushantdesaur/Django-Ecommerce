from .models import *
import json
from .utils import cart_data


def main(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
    return {
        'cart_items': cart_items,
    }
