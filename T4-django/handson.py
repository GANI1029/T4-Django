# models.py
from django.db import models

class GadgetModel(models.Model):
    gadget_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    color = models.CharField(max_length=50)
    warranty_period = models.FloatField()
    emi_available = models.BooleanField()
    rating = models.FloatField()

    def __str__(self):
        return self.gadget_name

# serializers.py
from rest_framework import serializers
from .models import GadgetModel

class GadgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GadgetModel
        fields = '__all__'

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GadgetModel
from .serializers import GadgetSerializer

class GadgetAddView(APIView):
    def post(self, request):
        serializer = GadgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GadgetListView(APIView):
    def get(self, request):
        gadgets = GadgetModel.objects.all()
        serializer = GadgetSerializer(gadgets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GadgetUpdateView(APIView):
    def patch(self, request, id):
        try:
            gadget = GadgetModel.objects.get(id=id)
        except GadgetModel.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GadgetSerializer(gadget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GadgetDeleteView(APIView):
    def delete(self, request, id):
        try:
            gadget = GadgetModel.objects.get(id=id)
        except GadgetModel.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        gadget.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# urls.py
from django.urls import path
from .views import GadgetAddView, GadgetListView, GadgetUpdateView, GadgetDeleteView

urlpatterns = [
    path('gadget/add/', GadgetAddView.as_view(), name='gadget_add'),
    path('gadget/list/', GadgetListView.as_view(), name='gadget_list'),
    path('gadget/update/<int:id>/', GadgetUpdateView.as_view(), name='gadget_update'),
    path('gadget/remove/<int:id>/', GadgetDeleteView.as_view(), name='gadget_remove'),
]
