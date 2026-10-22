import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import CustomerForm, OrderForm
from .models import Category, Customer, Order, OrderProduct, Product


def get_cart(request):
    """Read the 'orders' cookie and return [{'product': Product, 'count': int}, ...].

    A broken cookie, unknown product ids (deleted by staff) and counts below 1
    are skipped instead of crashing the page.
    """
    try:
        raw = json.loads(request.COOKIES.get("orders") or "{}")
    except ValueError:
        return []
    if not isinstance(raw, dict):
        return []

    counts = {}
    for key, value in raw.items():
        try:
            pk, count = int(key), int(value)
        except (TypeError, ValueError):
            continue
        if count >= 1:
            counts[pk] = count

    products = Product.objects.in_bulk(counts.keys())  # one query for the whole cart
    return [
        {"product": products[pk], "count": count}
        for pk, count in counts.items()
        if pk in products
    ]


def home_page(request):
    """JSON for one product, used by the cart JavaScript. Never returns `cost`."""
    product_id = request.GET.get("product_id", "")
    if not product_id.isdigit():
        return JsonResponse({"error": "product_id is required"}, status=400)

    product = (
        Product.objects.filter(pk=product_id)
        .values("id", "title", "description", "price", "image")
        .first()
    )
    if product is None:
        return JsonResponse({}, status=404)
    return JsonResponse(product)


def order_page(request):
    """JSON used to pre-fill the checkout form. Returns the first name only."""
    phone_number = request.GET.get("phone_number", "")
    if not phone_number:
        return JsonResponse({"error": "phone_number is required"}, status=400)

    customer = (
        Customer.objects.filter(phone_number=phone_number)
        .values("first_name")
        .first()
    )
    if customer is None:
        return JsonResponse({}, status=404)
    return JsonResponse(customer)


def index(request):
    ctx = {
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
        'orders': get_cart(request),
        'total_price': request.COOKIES.get("total_price", 0),
    }

    response = render(request, 'food/index.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response


def main_order(request):
    cart = get_cart(request)
    customer_form = order_form = None

    if request.method == "POST":
        if not cart:
            # Nothing to order (empty or broken cart cookie): do not save anything.
            return redirect("index")

        phone_number = request.POST.get("phone_number", "")
        customer = Customer.objects.filter(phone_number=phone_number).first()
        # A returning customer is only looked up: the public form never changes
        # the data of an existing customer.
        customer_form = None if customer else CustomerForm(request.POST)
        order_form = OrderForm(request.POST)

        # Validate everything BEFORE saving anything.
        customer_ok = customer_form is None or customer_form.is_valid()
        order_ok = order_form.is_valid()

        if customer_ok and order_ok:
            with transaction.atomic():  # all or nothing: no order without items
                if customer is None:
                    customer = customer_form.save()
                order = order_form.save(commit=False)
                order.customer = customer
                order.save()
                OrderProduct.objects.bulk_create([
                    OrderProduct(
                        order=order,
                        product=item["product"],
                        count=item["count"],
                        price=item["product"].price,  # current price from the database
                    )
                    for item in cart
                ])
            response = redirect("index")
            response.delete_cookie("orders")       # the cart is empty after ordering
            response.delete_cookie("total_price")
            return response

    ctx = {
        'orders': cart,
        'total_price': request.COOKIES.get("total_price", 0),
        # forms with .errors when validation failed (None on a normal GET)
        'customer_form': customer_form,
        'order_form': order_form,
    }

    response = render(request, 'food/order.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response
