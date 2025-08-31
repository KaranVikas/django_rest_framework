from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser , AllowAny
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination

# Create a class based view
class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  filterset_class = ProductFilter
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
  ordering_fields = ['name', 'price', 'stock']
  ordering = ['name']
  filterset_fields = [
    'name',
    'price',
    'stock',
  ]
  search_fields = ['=name', 'description']
  # pagination_class = PageNumberPagination
  # pagination_class.page_size = 2
  # pagination_class.page_query_param = 'pagenum'
  # pagination_class.page_size_query_param = 'size'
  # pagination_class.max_page_size = 4
  pagination_class = LimitOffsetPagination

  def get_permissions(self):
    self.permission_classes = [AllowAny]
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()


class ProductCreateAPIView(generics.CreateAPIView):
  model = Product
  serializer_class = ProductSerializer

  def create(self, request, *args, **kwargs):
    print(request.data)
    return super().create(request, *args, **kwargs)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_url_kwarg = 'product_id'

  def get_permissions(self):
    self.permission_classes = [AllowAny]
    if self.request.method in ['PUT', 'PATCH', 'DELETE']:
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    qs = super().get_queryset()
    return qs.filter(user=self.request.user)

# @api_view(['GET'])
# def product_info(request):
#   products = Product.objects.all()
#   serializer = ProductInfoSerializer({
#     'products': products,
#     'count': len(products),
#     'max_price': products.aggregate(max_price=Max('price'))['max_price']
#   })
#   return Response(serializer.data)

class ProductInfoAPIView(APIView):
  def get(self,request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
      'products':products,
      'count': len(products),
      'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)

