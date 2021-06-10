from django.shortcuts import render
from django.http import HttpRequest

from .models import Item


def item_list(request: HttpRequest):
    context = {"items": Item.objects.all()}
    return render(request, "item_list.html", context)
