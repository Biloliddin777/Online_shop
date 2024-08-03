from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from online_shop.forms import CommentModelForm, OrderModelForm, ProductModelForm
from online_shop.models import Category, Product, Comment


# Create your views here.


def product_list(request, category_id: Optional[int] = None):
    categories = Category.objects.all().order_by('id')
    if category_id:

        products = Product.objects.filter(category=category_id)

    else:
        products = Product.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'online_shop/home.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product_id, is_provide=True).order_by('-id')
    context = {
        'product': product,
        'comments': comments
    }

    return render(request, 'online_shop/detail.html', context)


# def add_comment(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         body = request.POST.get('body')
#         comment = Comment(name=name, email=email, body=body)
#         comment.product = product
#         comment.save()
#         return redirect('product_detail', product_id)
#     else:
#         pass
#     return render(request, 'online_shop/detail.html')

def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id)

    else:
        form = CommentModelForm()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'online_shop/detail.html', context)


def add_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm()

    if request.method == 'POST':

        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                # add messaging
                product.save()
                order.save()
                messages.add_message(
                    request,
                    level=messages.SUCCESS,
                    message='Your order is successfully saved'
                )

                return redirect('product_detail', product_id)
            else:
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message='Your order is not available'
                )

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'online_shop/detail.html', context)


@login_required
def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {
        'form': form
    }
    return render(request, 'online_shop/add-product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id)

    return render(request, 'online_shop/edit-product.html', {'form': form})