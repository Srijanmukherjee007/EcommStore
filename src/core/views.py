from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import HttpRequest

from .models import Item, OrderItem, Order


def item_list(request: HttpRequest):
    context = {"items": Item.objects.all()}
    return render(request, "home.html", context)


def products(request: HttpRequest):
    return render(request, "product.html")


def checkout(request: HttpRequest):
    return render(request, "checkout.html")


class HomeView(ListView):
    model = Item
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request: HttpRequest, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This item was added to cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, "This item was added to cart")
        return redirect("core:product", slug=slug)


def remove_from_cart(request: HttpRequest, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item is removed from your cart")
        else:
            messages.error(
                request, "This item is not in your cart", extra_tags="danger"
            )
        return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
