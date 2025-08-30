from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def product_list(request):
  # fetch all the products
  products = Product.objects.all()
  # create a serialiser ,many=True bcx many objects
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
  # fetch all the products
  product = get_object_or_404(Product, pk=pk)
  # create a serialiser ,many=True bcx many objects
  serializer = ProductSerializer(product)
  return Response(serializer.data)

@api_view(['Get'])
def order_list(request):
  orders = Order.objects.all()
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data)


