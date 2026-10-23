from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Count, F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from food.models import *
from . import forms
from . import services

def login_required_decarator(func):
    return login_required(func, login_url='login_page')

def paginate(request, queryset, per_page=20):
    """One page of a queryset; the page number comes from ?page=N."""
    return Paginator(queryset, per_page).get_page(request.GET.get("page"))

@login_required_decarator
def main_dashboard(request):
    # one query: every category with the number of its products
    categories_products = [
        {"category": c.title, "product": c.n}
        for c in Category.objects.annotate(n=Count("product"))
    ]
    # top 10 products by units sold (sum of the counts, not the number of order lines)
    table_list = (
        OrderProduct.objects.filter(product__isnull=False)
        .values("product_id", title=F("product__title"))
        .annotate(sold=Sum("count"))
        .order_by("-sold")[:10]
    )

    ctx = {
        "counts": {
            "categories": Category.objects.count(),
            "products": Product.objects.count(),
            "customers": Customer.objects.count(),
            "orders": Order.objects.count(),
        },
        "categories_products": categories_products,
        "table_list": table_list,
    }
    return render(request, 'dashboard/index.html', ctx)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('main_dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        # follow ?next= only when it points to this site
        if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            return redirect(next_url)
        return redirect('main_dashboard')

    return render(request, 'dashboard/login.html', {'form': form, 'next': next_url})

@login_required_decarator
def logout_page(request):
    logout(request)
    return redirect('login_page')

# ############ categories ############
@login_required_decarator
def category_list(request):
    categories = paginate(request, Category.objects.order_by("id"))
    ctx = {'kind': 'category', 'title': 'Categories', 'page': categories}
    return render(request, "dashboard/list.html", ctx)

@login_required_decarator
def category_create(request):
    """This is the metod for creating product categories: Pizzas, Burgers..."""
    model = Category()
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save() # form is saved
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Category',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
def category_edit(request, pk):
    model = get_object_or_404(Category, pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Category',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
@require_POST
def category_delete(request, pk):
    model = get_object_or_404(Category, pk=pk)
    model.delete()
    return redirect("category_list")

# ############ products ############
@login_required_decarator
def product_list(request):
    products = paginate(request, Product.objects.order_by("id"))
    ctx = {'kind': 'product', 'title': 'Products', 'page': products}
    return render(request, "dashboard/list.html", ctx)

@login_required_decarator
def product_create(request):
    model = Product()
    form = forms.ProductForm(request.POST or None, request.FILES or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('product_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Product',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
def product_edit(request, pk):
    model = get_object_or_404(Product, pk=pk)
    form = forms.ProductForm(request.POST or None, request.FILES or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('product_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Product',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
@require_POST
def product_delete(request, pk):
    model = get_object_or_404(Product, pk=pk)
    model.delete()
    return redirect("product_list")

# ############ customers (called "user" in the URLs) ############
@login_required_decarator
def user_list(request):
    users = paginate(request, Customer.objects.order_by("id"))
    ctx = {'kind': 'user', 'title': 'Customers', 'page': users}
    return render(request, "dashboard/list.html", ctx)

@login_required_decarator
def user_create(request):
    model = Customer()
    form = forms.UserForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Customer',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
def user_edit(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    form = forms.UserForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form,
        'entity': 'Customer',
    }
    return render(request, 'dashboard/form.html', ctx)

@login_required_decarator
@require_POST
def user_delete(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    model.delete()
    return redirect("user_list")

# ############ orders ############
@login_required_decarator
def order_list(request):
    orders = paginate(
        request,
        Order.objects.select_related("customer")   # one query instead of one per row
        .annotate(total=Sum(F("orderproduct__count") * F("orderproduct__price")))
        .order_by("-id"),
    )
    ctx = {'kind': 'order', 'title': 'Orders', 'page': orders}
    return render(request, "dashboard/list.html", ctx)

@login_required_decarator
def customer_order_list(request, id):
    customer_orders = services.get_order_by_user(id=id)
    ctx = {'kind': 'customer_order', 'title': 'Customer orders', 'page': customer_orders}
    return render(request, "dashboard/list.html", ctx)

@login_required_decarator
def orderproduct_list(request, id):
    productorders = services.get_product_by_order(id=id)
    ctx = {'kind': 'productorder', 'title': 'Order items', 'page': productorders}
    return render(request, "dashboard/list.html", ctx)
