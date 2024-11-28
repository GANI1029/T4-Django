from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer

@api_view(['GET', 'POST'])
def inventory_items(request):
    if request.method == 'GET':
        items = Inventory.objects.all()
        serializer = InventorySerializer(items, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = InventorySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            errors.setdefault('non_field_errors', [])
            errors['non_field_errors'].append('inventory with this barcode already exists')
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def inventory_item_detail(request, pk):
    try:
        item = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventorySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def inventory_items_sort(request):
    items = Inventory.objects.order_by('-price')
    serializer = InventorySerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def inventory_items_query_category(request, category):
    items = Inventory.objects.filter(category__icontains=category)
    print(items)
    serializer = InventorySerializer(items, many=True)
    return Response(serializer.data)
