import django_filters
from rest_framework import filters
from api.models import Product

class InStockFilterBackend(filters.BaseFilterBackend):
  def filter_queryset(self, request, queryset, view):
    return queryset.exclude(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
  class Meta:
    model = Product
    fields = {
      'name': ['iexact', 'contains'],
      'price': ['exact','lt','gt','range'],
    }

