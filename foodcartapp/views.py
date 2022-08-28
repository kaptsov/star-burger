from django.http import JsonResponse
from django.templatetags.static import static
from .models import OrderItem, Order, Customer
from rest_framework.decorators import api_view

import json

from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):

    data = request.data
    print(data)
    customer, _ = Customer.objects.update_or_create(
        name=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber'],
        address=data['address'],
    )
    print(customer.pk)
    order, _ = Order.objects.update_or_create(
        customer=Customer.objects.get(pk=customer.pk),
    )

    for order_item in data['products']:
        OrderItem.objects.update_or_create(
            order=Order.objects.get(pk=order.pk),
            product=Product.objects.get(pk=order_item['product']),
            quantity=order_item['quantity'],
            price=200
        )

    return JsonResponse(data)

