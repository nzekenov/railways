from django.shortcuts import render
from django.http import JsonResponse
from .models import Item

def index(request):
    return render(request, 'index.html')

def get_children(item):
    return [{
        'id': child.id,
        'text': child.code,
        'children': get_children(child)
    } for child in item.children.all()]

def tree_data(request):
    root_items = Item.objects.filter(parent__isnull=True)
    data = [{
        'id': item.id,
        'text': item.code,
        'children': get_children(item)
    } for item in root_items]
    return JsonResponse(data, safe=False)
