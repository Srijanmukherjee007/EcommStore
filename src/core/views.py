from django.shortcuts import render
from django.http import HttpRequest

from .models import Item


def item_list(request: HttpRequest):
    context = {"items": Item.objects.all()}
    return render(request, "home.html", context)


def products(request: HttpRequest):
    return render(request, "product.html")


def checkout(request: HttpRequest):
    return render(request, "checkout.html")
